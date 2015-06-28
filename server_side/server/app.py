# coding=utf-8
import json
import os
from uuid import uuid4
from twisted.cred.credentials import DigestedCredentials
from twisted.internet.defer import succeed
from functools import wraps
from twisted.web.resource import ForbiddenResource
from twisted.web.static import File
import hashlib, datetime


class Session:
    def __init__(self, user_name):
        self.user_name = user_name
        self.exp_time = None
        self.number = 0
        self.update_exp_time()

    def update_exp_time(self):
        self.exp_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        return self.exp_time


class App(object):
    class FileNoDir(File):
        def directoryListing(self):
            return ForbiddenResource()

    def __init__(self, server, root_path):
        """

        :type server: klein.app.Klein
        """
        self.root_path = root_path
        self.server = server
        self.setup_route(self.server)
        self.auth_users = dict()
        self.users = {
            'admin': 'admin'
        }

    def require_auth(self, *args, **kwargs):
        def call(f, *a, **kw):
            return f(*a, **kw)

        def deco(f):
            @wraps(f)
            def wrapped_f(request, *a, **kw):
                # do your authentication here
                if self.check_auth(request):
                    return call(f, request, *a, **kw)
                else:
                    request.setResponseCode(401)
                    return None

            return wrapped_f

        return deco

    def check_auth(self, request):
        is_auth_enabled = False
        if request.requestHeaders.hasHeader('x-session-token'):
            token_data = request.requestHeaders.getRawHeaders('x-session-token')[0]
            data = token_data.split('.')
            if len(data) == 3:
                token = data[0]
                md5 = data[1]
                number = data[2]
                try:
                    session = self.auth_users[token]
                    password = self.users[session.user_name]
                    str_to_md5 = '.'.join([token, password, number])
                    m = hashlib.md5()
                    m.update(str_to_md5)
                    expected_md5 = m.hexdigest()
                    if expected_md5 == md5:
                        try:
                            num = int(number)
                            if num >= session.number and datetime.datetime.now() < session.exp_time:
                                print 'authorized', session.number, num
                                is_auth_enabled = True
                                session.number = num + 1
                                session.update_exp_time()
                        except ValueError:
                            pass
                    if not is_auth_enabled:
                        try:
                            del self.auth_users[token]
                        except KeyError:
                            pass
                except KeyError:
                    pass

        return is_auth_enabled

    def login_get(self, request):
        return None

    def login_post(self, request):
        request.setResponseCode(200)
        token = uuid4().hex
        try:
            user_name = json.loads(request.content.read())['userName']
        except ValueError:
            user_name = None
        if user_name in self.users:
            self.auth_users[token] = Session(user_name)  # заменить на полезную нагрузку
            print('session created...')

        return json.dumps({'token': token})

    def login(self, request):
        """

        :type request: twisted.web.server.Request
        """

        @self.require_auth()
        def login_get(_request):
            return self.login_get(_request)

        if request.method == 'GET':
            return login_get(request)
        elif request.method == 'POST':
            return self.login_post(request)
        return json.dumps({'error': 'true'})

    def setup_route(self, server):
        @server.route('/', methods=['GET'])
        def index(_):
            index_path = os.path.join(self.root_path, 'templates', 'index.html')
            print index_path
            f = File(index_path)
            f.isLeaf = True
            return f

        @server.route('/api/1.0/login')
        def login_path(request):
            return self.login(request)

        @server.route('/templates', branch=True)
        def templates_path(_):
            return File(os.path.join(self.root_path, 'templates'))

        @server.route('/static', branch=True)
        def static_path(_):
            return File(os.path.join(self.root_path, 'static'))

        @server.route('/app', branch=True)
        def app_path(_):
            return File(os.path.join(self.root_path, 'app'))

        @server.route('/hello/word', methods=['GET'])
        def test(request):
            """

            :type request: twisted.web.server.Request
            """
            user = request.getHeader('user')
            return 'help me plz! {0}'.format(user)

        @server.route('/user/<string:name>', methods=['GET'])
        def hello_user(request, name):
            """

            :type request: twisted.web.server.Request
            """
            request.setHeader('user', name)
            request.redirect('/hello/word')
            return succeed(None)

        @server.route('/auth')
        def auth_res(response):
            """

            :type response: twisted.web.server.Request
            """
            print(response.getAllHeaders())
            response.setHeader('WWW-Authenticate',
                               'Digest realm="svs@svs35.ru",'
                               'qop="auth",'
                               'nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093",'
                               'opaque="5ccc069c403ebaf9f0171e9517f40e41"')
            response.setResponseCode(401)
            return "Fuck you"
