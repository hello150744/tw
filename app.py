# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import os
from twisted.internet import reactor, protocol
local_hostname =os.getenv("OPENSHIFT_PYTHON_IP")
local_port=os.getenv("OPENSHIFT_PYTHON_PORT")

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write(data)


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8080,factory,interface='54.84.110.33')
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
