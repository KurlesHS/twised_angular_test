import os
from server.server import Server
from server.app import App

if __name__ == '__main__':
    client_side_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client_side'))
    server = Server(client_side_dir)
    app = App()
    server.run()
