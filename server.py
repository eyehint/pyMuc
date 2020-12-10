import gc

from twisted.application import service, internet
from twisted.internet import protocol, reactor

from client import Client
from loop import Loop
from objs.emotion import Emotion
from objs.item import loadAllItem
from objs.mob import loadAllMob
from objs.player import init_commands

gc.enable()
init_commands()
Emotion()

loadAllMob()
loadAllItem()

Loop()

factory = protocol.ServerFactory()
factory.protocol = Client
application = service.Application("pyMUC_Server")
server = internet.TCPServer(9999, factory)
server.setServiceParent(application)

reactor.listenTCP(9999, factory)
reactor.run()
