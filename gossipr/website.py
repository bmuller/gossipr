from twisted.python import log

from nevow import rend, loaders, tags as T
from nevow.static import File

from gossipr.models import Message
import gossipr, os

class MessageLister(rend.Page):
    docFactory = loaders.stan(
        T.html[ T.head[ T.link(href="static/style.css", type="text/css", rel="stylesheet") ],
          T.div(render=T.directive('form')),
          T.table(render=T.directive('sequence'))[
            T.tr(pattern='header')[ T.th[ 'speaker' ], T.th[ 'Date Time' ], T.th[ 'Message' ] ],
            T.tr(pattern='item', class_='odd', render=T.directive('row')),
            T.tr(pattern='item', class_='even', render=T.directive('row'))
          ]
        ])        


    def __init__(self, msgs, query, startdate, enddate):
        self.query = query
        self.startdate = startdate
        self.enddate = enddate
        rend.Page.__init__(self, msgs)
    

    def render_row(self, context, msg):
        return context.tag[ T.td[ msg[0] ], T.td[ msg[1] ], T.td[ msg[2] ] ]

    def render_form(self, context, data):
        return context.tag[
              T.form(action="/")[
                "Query: ", T.input(type="text", name="query", value=self.query),
                "Start Date: ", T.input(type="text", name="startdate", value=self.startdate),
                "End Date: ", T.input(type="text", name="enddate", value=self.enddate),
                T.input(type="submit", value="Search") 
              ]
            ]



class MainPage(rend.Page):
    addSlash = True
    
    def __init__(self, config):
        self.config = config
        rend.Page.__init__(self)

    def locateChild(self, ctx, segments):
        if segments[0] == "static":
            static = os.path.join(gossipr.__path__[0], "static")
            return File(static), segments[1:]

        args = [ctx.arg('query', ''), ctx.arg('startdate', ''), ctx.arg('enddate', '')]
        def handleMsgs(msgs):
            rows = []
            for msg in msgs:
                created_at = msg.created_at.isoformat()
                rows.append((msg.speaker, created_at, msg.message))
            return MessageLister(rows, *args), ""
        return Message.doSearch(*args).addCallback(handleMsgs)
