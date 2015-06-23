import os
from twisted.web.server import Site
from twisted.web.resource import ForbiddenResource, Resource
from twisted.web.static import File
from twisted.internet import reactor


class FileNoDir(File):
    def directoryListing(self):
        return ForbiddenResource()


class Root(Resource):
    server_instance = None

    def getChild(self, path, request):
        """

        :type request: twisted.web.server.Request
        """
        print 'getChild', path, request
        paths = request.prepath + request.postpath
        paths.remove('')
        s = '/' + '/'.join(paths)

        try:
            r = Server.routes[s]
            return r
        except KeyError:
            pass

        return Resource.getChild(self, path, request)


class Server(object):
    instance = None
    routes = {}

    def __init__(self, client_side_path):
        self.client_side_path = client_side_path
        self.site = None
        self.routes = {}
        Server.instance = self

    def run(self):
        root = Root()
        Root.server_instance = self
        self.site = Site(root)
        root.putChild("static", FileNoDir(os.path.join(self.client_side_path, 'static')))
        root.putChild("app", FileNoDir(os.path.join(self.client_side_path, 'app')))
        root.putChild("", File(os.path.join(self.client_side_path, 'templates', 'index.html')))
        root.putChild("templates", File(os.path.join(self.client_side_path, 'templates')))
        reactor.listenTCP(8888, self.site)
        reactor.run()

    @staticmethod
    def route(fn):
        def wrapper(path):
            """

            :type path: str
            """
            r = Resource()
            r.render = path
            r.isLeaf = True
            Server.routes[fn] = r
            return fn

        return wrapper
