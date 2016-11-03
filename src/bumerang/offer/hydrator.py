from bumerang.error import InvalidRecordError
from bumerang.offer.offer import Offer


class Hydrator:

    def __init__(self, record):
        self._record = record

    def to_request(self):
        try:
            id, profile_id, borrow_id = self._record
            return Offer(id, profile_id, borrow_id)
        except ValueError as e:
            raise InvalidRecordError(str(e))
