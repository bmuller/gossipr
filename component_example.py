import time
from twisted.words.protocols.jabber import jid, xmlstream
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.application import internet, service
from twisted.internet import interfaces, defer, reactor
from twisted.python import log
from twisted.words.xish import domish


from twisted.words.protocols.jabber.ijabber import IService
from twisted.words.protocols.jabber import component

from zope.interface import Interface, implements

#PRESENCE = '/presence' # this is an global xpath query to use in an observer
#MESSAGE  = '/message'  # message xpath
#IQ       = '/iq'       # iq xpath

class LogService(component.Service):
    """
    A service to log incoming and outgoing xml to and from our XMPP component.
    """
    
    def transportConnected(self, xmlstream):
        xmlstream.rawDataInFn = self.rawDataIn
        xmlstream.rawDataOutFn = self.rawDataOut
        
    def rawDataIn(self, buf):
        log.msg("%s - RECV: %s" % (str(time.time()), unicode(buf, 'utf-8').encode('ascii', 'replace')))
        
    def rawDataOut(self, buf):
        log.msg("%s - SEND: %s" % (str(time.time()), unicode(buf, 'utf-8').encode('ascii', 'replace')))
        

class ExampleService(component.Service):
    implements(IService)


    def componentConnected(self, xmlstream):
        self.jabberId = xmlstream.authenticator.otherHost
        self.xmlstream = xmlstream # set the xmlstream so we can reuse it

        #xmlstream.addObserver(PRESENCE, self.onPresence, 1)
        #xmlstream.addObserver(IQ, self.onIq, 1)
        #xmlstream.addObserver(MESSAGE, self.onMessage, 1)

        #p = domish.Element((None, 'presence'))
        #p['to'] = 'awesome@conference.localhost/listener'
        #p['from'] = 'listener@gossipr.localhost/listener'
        #p.addElement('x', 'http://jabber.org/protocol/muc')
        #xmlstream.send(p)

        iq = IQ(self.xmlstream, 'get')
        iq['from'] = 'listener@gossipr.localhost/listener'
        iq.addElement('query', 'http://jabber.org/protocol/disco#items')
        iq.send('conference.localhost')

    def onMessage(self, msg):
        pass

