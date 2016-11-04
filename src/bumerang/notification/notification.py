class Notification:

    def __init__(self, msg, to, type, priority='high', ttl=0):
        self.msg = msg
        self.to = to
        self.type = type
        self.priority = priority
        self.ttl = ttl

    def __repr__(self):
        pass

    def to_body(self):
        return {
            'to': self.to,
            'time_to_live': self.ttl,
            'data': {'text': self.msg, 'type': self.type}
        }
