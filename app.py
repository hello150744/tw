from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
host='59.66.193.197'
port=8080

class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s\n" % msg)
    def dataReceived(self,data):
        log=open('log','w+')
        log.write(data)
        log.close()

def gotProtocol(p):
    p.sendMessage("Hello")
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

point = TCP4ClientEndpoint(reactor, host, port)
d = connectProtocol(point, Greeter())
d.addCallback(gotProtocol)
reactor.run()
