from server import Server

# from twisted.web.server import NOT_DONE_YET


class App(object):
    def __init__(self, server):
        """

        :type server: Server
        """
        self.server = server
        self.setup_route(self.server)

    @staticmethod
    def setup_route(server):
        @server.route('/hello/word')
        def test(request):

            """

            :type request: twisted.web.server.Request
            """
            if request.method == 'GET2':
                request.setHeader('Custom', 'True')
                return 'hello world'
            else:
                request.setResponseCode(404)
                return 'error'
