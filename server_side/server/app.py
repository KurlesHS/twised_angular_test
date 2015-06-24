class App(object):
    def __init__(self, server):
        """

        :type server: klein.app.Klein
        """
        self.server = server
        self.setup_route(self.server)

    @staticmethod
    def setup_route(server):
        @server.route('/hello/word', methods=['GET'])
        def test(request):
            return 'help me plz!'
