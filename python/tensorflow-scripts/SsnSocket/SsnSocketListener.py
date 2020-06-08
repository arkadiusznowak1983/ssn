import socket
from random import randrange

class SsnSocketListener:
    # config dict data
    _configuration = {}
    def initConfiguration(self):
        self._configuration.update( {'TCP_IP': socket.gethostname(),
                                    #'TCP_PORT': randrange(10000, 60000),
                                    'MAX_LISTENERS': 1,
                                    'BUFFOR': 1024} )

    def setPort( self, port ):
        self._configuration.update( {'TCP_PORT': port } )

    def getConfiguration( self ):
        return self._configuration

    def printConfiguration( self ):
        print( self._configuration )

    def bind( self ):
        self.sock.bind(( self._configuration['TCP_IP'], self._configuration['TCP_PORT'] ))
        
    def __init__( self, sock=None ):
        if sock is None:
            self.initConfiguration()
            self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        else:
            self.sock = sock

    def listen( self ):
        self.sock.listen( self._configuration['MAX_LISTENERS'] )
        self.clientsocket, self.address = self.sock.accept()

        #while True:
        data_received = self.clientsocket.recv( self._configuration['BUFFOR'] )
        #    if not data_received:
        print( data_received )
        #        break
        self.clientsocket.sendall('Witam Pana'.encode());
        
        self.clientsocket.close()

