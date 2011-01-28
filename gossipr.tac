from twisted.application import service, internet
from twisted.words.protocols.jabber import component
from twisted.enterprise import adbapi

from nevow import appserver

from twistar.registry import Registry

from gossipr import listener, website

from config import CONFIG

# connect to DB
Registry.DBPOOL = adbapi.ConnectionPool(CONFIG['db.driver'], 
                                        user=CONFIG['db.user'],
                                        passwd=CONFIG['db.pass'],
                                        db=CONFIG['db.name'],
                                        host=CONFIG['db.host'])

# Application set up
application = service.Application("gossipr")


# Component
host = "tcp:%s:%s" % (CONFIG['xmpp.host'], CONFIG['xmpp.port'])
#sm = component.buildServiceManager(CONFIG['xmpp.gossipr.host'], CONFIG['xmpp.password'], (host))
#listener.LogService().setServiceParent(sm)
#s = listener.ListenerService(CONFIG)
#s.setServiceParent(sm)
#sm.setServiceParent(application)

# Website
website = appserver.NevowSite(website.MainPage(CONFIG))
internet.TCPServer(CONFIG['web.port'], website).setServiceParent(application)
