import os
from twisted.web.server import Site
from twisted.web.resource import ForbiddenResource, Resource
from twisted.web.static import File
from twisted.internet import reactor


class FileNoDir(File):
    def directoryListing(self):
        return ForbiddenResource()


class Root(Resource):
    def __init__(self, server):
        """

            :type server: Server
            """
        Resource.__init__(self)
        self.server = server

    def getChild(self, path, request):
        """

        :type request: twisted.web.server.Request
        """
        print 'getChild', path, request
        paths = request.prepath + request.postpath
        try:
            paths.remove('')
        except ValueError:
            pass
        s = '/' + '/'.join(paths)

        try:
            r = self.server.routes[s]
            return r
        except KeyError:
            pass

        return Resource.getChild(self, path, request)


class Server(object):
    def __init__(self, client_side_path):
        self.client_side_path = client_side_path
        self.site = None
        self.routes = {}
        Server.instance = self

    def run(self):
        root = Root(self)
        self.site = Site(root)
        root.putChild("static", FileNoDir(os.path.join(self.client_side_path, 'static')))
        root.putChild("app", FileNoDir(os.path.join(self.client_side_path, 'app')))
        root.putChild("", File(os.path.join(self.client_side_path, 'templates', 'index.html')))
        root.putChild("templates", File(os.path.join(self.client_side_path, 'templates')))
        reactor.listenTCP(8888, self.site)
        reactor.run()

    def route(self, path):
        def wrapper(fn):
            """

            :type path: str
            """
            r = Resource()
            r.render_GET = fn
            r.isLeaf = True
            self.routes[path] = r
            return fn
        return wrapper
