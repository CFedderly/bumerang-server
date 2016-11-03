from bumerang.error import InvalidRecordError
from bumerang.profile.profile import Profile


class Hydrator:

    def __init__(self, record):
        self._record = record

    def to_request(self):
        """Converts a record into a profile request

        Throws InvalidRecordError
        """
        try:
            (
                id, facebook_id, device_id, first_name,
                last_name, description, phone_number, karma,
            ) = self._record
            return Profile(
                id, facebook_id, device_id,
                first_name, last_name, description,
                phone_number, karma
            )

        except ValueError as e:
            raise InvalidRecordError(str(e))
