from bumerang.db.databasequery import DatabaseQuery
from bumerang.error import InvalidIDConstraintError
from bumerang.profile.hydrator import Hydrator


class ProfileRepo:

    def __init__(self, db, table):
        self._db = db
        self._table = table

    def find_one_by_id(self, id):
        """Find a profile by its id

            TODO create a baseclass for this logic and hydrator
        """
        query = DatabaseQuery(self._db)
        query.select("""
            SELECT ID, FACEBOOK_ID, DEVICE_ID, FIRST_NAME, LAST_NAME
            FROM {table} WHERE ID = %(id)s
        """.format(table=self._table), {'id': id}
        )

        if len(records) > 1:
            raise InvalidIDConstraintError(id)

        if records:
            hydrator = Hydrator(records[0])
            return hydrator.to_request()
        else:
            return None
