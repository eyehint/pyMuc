from twisted.internet import protocol
from twisted.application import service, internet
import gc

from client import Client, queue
from loop import Loop
from objs.config import Config
from objs.skill import Skill
from objs.help import Help
from objs.script import Script
from objs.doumi import Doumi
from objs.emotion import Emotion
from objs.player import init_commands
from objs.nickname import Nickname
from objs.oneitem import Oneitem
from objs.rank import Rank
from objs.guild import Guild
from objs.mob import loadAllMob
from objs.item import loadAllItem

gc.enable()
init_commands()
Emotion()

loadAllMob()
loadAllItem()

Loop()

factory = protocol.ServerFactory()
factory.protocol = Client
application = service.Application("pyMUC_Server")
internet.TCPServer(9999, factory).setServiceParent(application)
