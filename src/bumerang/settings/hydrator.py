from bumerang.error import InvalidRecordError
from bumerang.settings.settings import Settings


class Hydrator:

    def __init__(self, record):
        self._record = record

    def to_request(self):
        """Hydrate the record into a settings object"""
        try:
            profile_id, request_noti, offer_noti = self._record
            return Settings(profile_id, request_noti, offer_noti)
        except ValueError as e:
            raise InvalidRecordError(str(e))
