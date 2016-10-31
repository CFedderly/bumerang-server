class BumerangError(Exception):
    """A base class for other classes to extend"""
    pass


class InvalidIDConstraintError(BumerangError):

    def __init__(self, id):
        super().__init__()
        self._id = id

    def __repr__(self):
        return 'InvalidIDConstraintError(%r)' % self._id

    def __str__(self):
        return (
            'Invalid ID Constraint Error: More than one record with the id'
            ' {id}'.format(id=self._id)
        )


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
