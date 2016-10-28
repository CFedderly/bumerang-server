class BumerangError(Exception):
    """A base class for other classes to extend"""
    pass


class InvalidRecordError(BumerangError):

    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __repr__(self):
        return 'InvalidRecordError(%r)' % self._msg

    def __str__(self):
        return 'Invalid Record Error: {msg}'.format(msg=self._msg)


class InvalidQueryError(BumerangError):

    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __repr__(self):
        return 'InvalidQueryError(%r)' % self._msg

    def __str__(self):
        return 'Invalid Query: {msg}'.format(msg=self._msg)
