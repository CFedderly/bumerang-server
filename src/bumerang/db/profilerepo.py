from bumerang.db.databasequery import DatabaseQuery
from bumerang.error import InvalidIDConstraintError
from bumerang.profile.hydrator import Hydrator


class ProfileRepo:

    def __init__(self, db, table):
        self._db = db
        self._table = table

    def edit_one(self, id, profile_node):
        pass

    def find_one_by_id(self, id):
        """Find a profile by its id

            TODO create a baseclass for this logic and hydrator
        """
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT ID, FACEBOOK_ID, DEVICE_ID, FIRST_NAME, LAST_NAME,
            DESCRIPTION FROM {table}
            WHERE ID = %(id)s
        """.format(table=self._table), {'id': id}
        )

        if len(records) > 1:
            raise InvalidIDConstraintError(id)

        if records:
            hydrator = Hydrator(records[0])
            return hydrator.to_request()
        else:
            return None

    def insert_one(self, profile_node):
        """Create a profile

        Throws InvalidQueryError
        """
        query = DatabaseQuery(self._db)
        record = query.insert("""
            INSERT INTO {table}
            (FACEBOOK_ID, DEVICE_ID, FIRST_NAME, LAST_NAME, DESCRIPTION)
            VALUES (%(facebook_id)s, %(device_id)s, %(first_name)s,
                %(last_name)s, %(description)s)
            RETURNING ID
        """.format(table=self._table), profile_node
        )

        return record[0]
