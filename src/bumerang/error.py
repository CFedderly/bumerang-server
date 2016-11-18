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


class InvalidRequestTypeError(BumerangError):

    def __init__(self, req_type):
        super().__init__()
        self._req_type = req_type

    def __repr__(self):
        return 'InvalidRequestTypeError(%r)' % self._req_type

    def __str__(self):
        return 'Invalid Request Type {}'.format(self._req_type)


class InvalidQueryError(BumerangError):

    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __repr__(self):
        return 'InvalidQueryError(%r)' % self._msg

    def __str__(self):
        return 'Invalid Query: {msg}'.format(msg=self._msg)
