import os
from twisted.cred.credentials import DigestedCredentials
from twisted.internet.defer import succeed
from functools import wraps
from twisted.web.resource import ForbiddenResource
from twisted.web.static import File


def require_auth(*args, **kwargs):
    def call(f, *a, **kw):
        return f(*a, **kw)

    def deco(f):
        @wraps(f)
        def wrapped_f(request, *a, **kw):
            # do your authentication here

            return call(f, request, *a, **kw)

        return wrapped_f

    return deco


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

    def setup_route(self, server):
        @server.route('/', methods=['GET'])
        def index(_):
            index_path = os.path.join(self.root_path, 'templates', 'index.html')
            print index_path
            file = File(index_path);
            file.isLeaf = True
            print file.exists()
            return file

        @server.route('/templates', branch=True)
        def templates_path(_):
            return App.FileNoDir(os.path.join(self.root_path, 'templates'))

        @server.route('/static', branch=True)
        def templates_path(_):
            return App.FileNoDir(os.path.join(self.root_path, 'static'))

        @server.route('/app', branch=True)
        def app_path(_):
            return App.FileNoDir(os.path.join(self.root_path, 'app'))

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
