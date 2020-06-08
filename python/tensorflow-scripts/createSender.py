from SsnSocket import SsnSocketSender

sender = SsnSocketSender()
sender.connect( 'flipbook', 12321 )
sender.mysend( 'arek tu byl' )



