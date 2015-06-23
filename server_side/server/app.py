from server import Server


class App(object):
    def __init__(self):
        pass

    @Server.route('/hello/word')
    def test(self):
        return 'hello world'
