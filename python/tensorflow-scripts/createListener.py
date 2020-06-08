from SsnSocket import SsnSocketListener

if __name__ == '__main__':
    listener = SsnSocketListener()
    listener.setPort( 12321 )
    listener.bind()
    listener.printConfiguration()
    
    listener.listen()

