# coding=utf-8
import os

from klein import Klein
from twisted.internet import reactor
from twisted.web.resource import Resource, ForbiddenResource
from twisted.web.server import Site
from twisted.web.static import File

from server.app import App

class FileNoDir(File):
    def directoryListing(self):
        return ForbiddenResource()

if __name__ == '__main__':
    client_side_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client_side'))
    server = Klein()
    app = App(server, client_side_dir)
    root = server.resource()
    site = Site(root)
    """
    root.putChild("static", FileNoDir(os.path.join(client_side_dir, 'static')))
    root.putChild("app", FileNoDir(os.path.join(client_side_dir, 'app')))
    root.putChild("", File(os.path.join(client_side_dir, 'templates', 'index.html')))
    root.putChild("templates", File(os.path.join(client_side_dir, 'templates')))
    """
    reactor.listenTCP(8888, site)
    reactor.run()
