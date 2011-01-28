from twistar.dbobject import DBObject
from twistar.registry import Registry

class Room(DBObject):
    HASMANY = ['messages']

    @classmethod
    def createIfNonexistant(klass, jid, name):
        def _createIfNonexistant(result):
            if result is None:
                return Room(jid=jid, name=name).save()
            return result
        return Room.find(where=['jid = ?', jid], limit=1).addCallback(_createIfNonexistant)
        

class Message(DBObject):
    BELONGSTO = ['room']
