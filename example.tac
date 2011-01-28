from twisted.application import service
from twisted.words.protocols.jabber import component
import component_example

application = service.Application("example-echo")
# set up Jabber Component
sm = component.buildServiceManager('gossipr.localhost', 'secret',
                                   ("tcp:127.0.0.1:5524" ))


# Turn on verbose mode
component_example.LogService().setServiceParent(sm)

# set up our example Service
s = component_example.ExampleService()
s.setServiceParent(sm)

sm.setServiceParent(application)
