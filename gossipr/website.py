from twisted.python import log

from nevow import rend, loaders, tags as T, stan
from nevow.static import File

from gossipr.models import Message, Room
import gossipr, os

HEADER = T.head[
    T.link(href="static/application.css", type="text/css", rel="stylesheet"),
    T.link(href="static/base.css", type="text/css", rel="stylesheet"),
    T.link(href="static/toupee/buttons.css", type="text/css", rel="stylesheet"),
    T.link(href="static/toupee/forms.css", type="text/css", rel="stylesheet"),
    T.link(href="static/toupee/modules.css", type="text/css", rel="stylesheet"),
    T.link(href="static/toupee/reset.css", type="text/css", rel="stylesheet"),
    T.link(href="static/toupee/structure.css", type="text/css", rel="stylesheet"),
    T.link(href="static/toupee/typography.css", type="text/css", rel="stylesheet"),            
    T.link(href="static/jquery-ui-1.8.9.custom.css", type="text/css", rel="stylesheet"),
    T.script(type="text/javascript", src="static/jquery-1.4.4.min.js"),
    T.script(type="text/javascript", src="static/jquery-ui-1.8.9.custom.min.js"),
    T.script(type="text/javascript", src="static/jquery-ui-timepicker-addon.js"),
    T.script(type="text/javascript", src="http://scripts.embed.ly/embedly.js")
]


class RoomLister(rend.Page):
    docFactory = loaders.stan(
        T.html[
          HEADER, T.body[
            T.div(class_='container')[
              stan.Tag('section', children = [
                T.h1[ 'Chat Logs: Room List'],
                stan.Tag('article', {'class': 'span-20'}, [
                  T.div(render=T.directive("roompicker"))
                ])
              ])
            ]
          ]
        ])


    def __init__(self, rooms):
        self.rooms = rooms
        rend.Page.__init__(self)
        

    def render_roompicker(self, context, data):
        options = []
        for room in self.rooms:
            link = "?room_id=%i" % room.id
            options.append(T.li[ T.a(href=link)[room.name] ])
        return context.tag[ T.ul[ options ]  ]



class MessageLister(rend.Page):
    docFactory = loaders.stan(
        T.html[
          HEADER, T.body[
            T.div(class_='container')[
              stan.Tag('section', children = [
                T.h1(render=T.directive('hone')),
                stan.Tag('article', {'class': 'span-20'}, [
                  T.div(render=T.directive('form'), id="qform"),
                  T.script(type="text/javascript")[ "$('#startdate').datetimepicker({ dateFormat: 'yy-mm-dd' })" ],
                  T.script(type="text/javascript")[ "$('#enddate').datetimepicker({ dateFormat: 'yy-mm-dd' });" ],            
                  T.table(render=T.directive('sequence'))[
                  T.tr(pattern='header')[ T.th(scope='col')[ 'speaker' ], T.th(scope='col')[ 'time' ], T.th(scope='col')[ 'message' ] ],
                    T.tr(pattern='item', render=T.directive('row')),
                    T.tr(pattern='item', class_='alt', render=T.directive('row'))
                  ]
                ])
              ])
            ]
          ]
        ])        


    def __init__(self, msgs, room, query, startdate, enddate, room_id):
        self.query = query
        self.startdate = startdate
        self.enddate = enddate
        self.room = room
        rend.Page.__init__(self, msgs)


    def render_hone(self, context, data):
        return context.tag[ "Chat Logs: %s" % self.room.name ]


    def render_row(self, context, msg):
        return context.tag[ T.td[ msg[0] ], T.td[ msg[1] ], T.td[ msg[2] ] ]


    def render_form(self, context, data):
        return context.tag[
              T.form(action="/")[
                T.span["Query: ", T.input(type="text", name="query", value=self.query)],
                T.span["Start Date: ", T.input(type="text", name="startdate", id="startdate", value=self.startdate, size="13")],
                T.span["End Date: ", T.input(type="text", name="enddate", id="enddate", value=self.enddate, size="13")],
                T.input(**{'type': "submit", 'value': "Search", 'class': "button second medium"}),
                T.input(type="hidden", name="room_id", value=self.room.id)
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
        if segments[0] == "images":
            images = os.path.join(gossipr.__path__[0], "static", "images")
            return File(images), segments[1:]
        
        if ctx.arg('room_id', '') == '':
            return Room.all().addCallback(lambda rooms: (RoomLister(rooms), ""))

        room_id = ctx.arg('room_id', '')
        args = [ctx.arg('query', ''), ctx.arg('startdate', ''), ctx.arg('enddate', ''), room_id]
        def handleMsgs(msgs):
            rows = []
            for msg in msgs:
                created_at = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
                rows.append((msg.speaker, created_at, self.format(msg.message)))
            return Room.find(room_id).addCallback(lambda room: (MessageLister(rows, room, *args), ""))
        return Message.doSearch(*args).addCallback(handleMsgs)


    def format(self, message):
        return map(self.formatAtom, message.split(' '))


    def formatAtom(self, atom):
        if atom.startswith('http://') or atom.startswith('https://'):
            return T.a(href=atom)[ atom ]
        return atom
        

