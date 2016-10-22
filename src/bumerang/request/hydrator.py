from bumerang.error import InvalidRecordError
from bumerang.request.borrowrequest import BorrowRequest


class Hydrator:

    def __init__(self, record):
        self._record = record

    def to_borrow_request(self):
        """Converts a record into a borrow request.

        Throws InvalidRecordError
        """
        try:
            id, title, description, distance, duration = self._record
            return BorrowRequest(id, title, description, distance, duration)
        except ValueError as e:
            raise InvalidRecordError(str(e))
