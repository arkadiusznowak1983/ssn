from SsnSocket import SsnSocketSender, SsnSocketListener

listener = SsnSocketListener()
listener.listen()
listener.printConfiguration()

sender = SsnSocketSender()

tcp_host, tcp_port = list( listener.getConfiguration().values() )[:2]
print (tcp_host, tcp_port)

sender.connect( tcp_host, tcp_port )
sender.mysend('dupa')
