from bumerang.db.databasequery import DatabaseQuery
from bumerang.offer.hydrator import Hydrator


class OfferRepo:

    def __init__(self, db, table):
        self._db = db
        self._table = table

    def find_one_by_id(self, id):
        """TODO add this to base class"""
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT o0_.id, o0_.profile_id, o0_.borrow_id
            FROM {table} o0_
            WHERE o0_.id = %(id)s
        """.format(table=self._table), {'id': id}
        )

        if len(records) > 1:
            raise InvalidIDConstraintError(id)

        if records:
            hydrator = Hydrator(records[0])
            return hydrator.to_request()
        else:
            return None

    def insert_one(self, node):
        """TODO add to base class"""
        query = DatabaseQuery(self._db)
        record = query.insert("""
            INSERT INTO {table} (PROFILE_ID, BORROW_ID)
            VALUES (%(profile_id)s, %(borrow_id)s)
            RETURNING ID
        """.format(table=self._table), node
        )

        return record[0]
