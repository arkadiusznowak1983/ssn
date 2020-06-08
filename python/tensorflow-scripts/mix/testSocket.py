from threading import Thread
from SsnSocket import SsnSocketListener, SsnSocketSender
from time import sleep


listener = SsnSocketListener()
listener.printConfiguration()

sender = SsnSocketSender()
sender.connect( 'flipbook', listener.getConfiguration()['TCP_PORT'] )

def thdListener():
    listener.listen()

def thdSender():
    sender.mysend( 'arek tu byl' )

threadListener = Thread(target = thdListener, args = ())
threadListener.start()
sleep(2)

threadSender = Thread(target = thdSender, args = ())
threadSender.start()
sleep(2)

threadListener.join()
threadSender.join()
