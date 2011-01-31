from twisted.python import log
from twisted.web2 import static, responsecode, http, resource, http_headers

from mako.lookup import TemplateLookup

from gossipr.models import Message, Room
import gossipr, os


TEMPLATES = TemplateLookup(directories=[os.path.join(gossipr.__path__[0], "templates")])

def render(template, **kwargs):
    temp = TEMPLATES.get_template(template)
    return http.Response(responsecode.OK,
                         {'content-type': http_headers.MimeType('text', 'html')},
                         temp.render(**kwargs))


class RoomLister(resource.Resource):
    def __init__(self, rooms):
        self.rooms = rooms
        resource.Resource.__init__(self)

        
    def render(self, req):
        links = {}
        for room in self.rooms:
            links[room.name] = "?room_id=%i" % room.id
        return render('roomlist.mako', links=links)


class MessageLister(resource.Resource):
    def __init__(self, msgs, room, query, startdate, enddate, room_id):
        self.query = query
        self.startdate = startdate
        self.enddate = enddate
        self.room = room
        self.msgs = msgs
        resource.Resource.__init__(self)


    def render(self, req):
        cleaned = []
        for msg in self.msgs:
            cleaned.append({'speaker': msg.speaker,
                            'created_at': msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            'msg': self.format(msg.message),
                            'id': int(msg.id)})
        return render('logs.mako', msgs=cleaned, startdate=self.startdate, enddate=self.enddate, query=self.query, room=self.room)


    def format(self, message):
        return " ".join(map(self.formatAtom, message.split(' ')))


    def formatAtom(self, atom):
        if atom.startswith('http://') or atom.startswith('https://'):
            return "<a href=\"%s\">%s</a>" % (atom, atom)
        return atom


class MainPage(resource.Resource):
    addSlash = True
    child_static = static.File(os.path.join(gossipr.__path__[0], "static"))
    child_images = static.File(os.path.join(gossipr.__path__[0], "static", "images"))
    
    def __init__(self, config):
        self.config = config
        resource.Resource.__init__(self)

    def render(self, req):
        room_id = req.args.get('room_id', [''])[0]
        if room_id == '':
            return Room.all().addCallback(lambda rooms: RoomLister(rooms))

        args = map(lambda x: req.args.get(x, [''])[0], ['query', 'startdate', 'enddate']) + [room_id]
        def handleMsgs(msgs):
            return Room.find(room_id).addCallback(lambda room: MessageLister(msgs, room, *args))
        return Message.doSearch(*args).addCallback(handleMsgs)





