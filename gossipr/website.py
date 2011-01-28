from nevow import rend, loaders, tags as T

from gossipr.models import Message

class MessageLister(rend.Page):
    docFactory = loaders.stan(
        T.html[
        T.table(render=T.directive('sequence'))[
        T.tr(pattern='header')[ T.th[ 'speaker' ], T.th[ 'Date Time' ], T.th[ 'Message' ] ],
        T.tr(pattern='item', class_='odd', render=T.directive('row')),
        T.tr(pattern='item', class_='even', render=T.directive('row'))
        ]
        ]
        )
    
    def render_row(self, context, aFile):
        return context.tag[ T.td[ aFile[0] ], T.td[ aFile[1] ], T.td[ aFile[2] ] ]


class MainPage(rend.Page):
    addSlash = True
    
    def __init__(self, config):
        self.config = config
        rend.Page.__init__(self)


    def locateChild(self, ctx, segments):
        if ctx.arg('hi', '') == "hi":
            return "hi", ""
        def handleMsgs(msgs):
            rows = []
            for msg in msgs:
                created_at = msg.created_at.isoformat()
                rows.append((msg.speaker, created_at, msg.message))
            return MessageLister(rows), ""
        return Message.all().addCallback(handleMsgs)
