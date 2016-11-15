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

    def find_offers_by_borrow_id(self, borrow_id):
        """ Finds the offers with the given borrow id

        :borrow_id type: int
        :borrow_id: The borrow id of the desired offers

        :rtype: list of Offers
        :return: A list of offers with the desired borrow id, or None if none found
        """
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT o0_.id, o0_.profile_id, o0_.borrow_id
            FROM {table} o0_
            WHERE o0_.borrow_id = %(borrow_id)s
        """.format(table=self._table), {'borrow_id': borrow_id}
        )

        if records:
            hydrators = [Hydrator(x) for x in records]
            return [x.to_request() for x in hydrators]
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

    def remove_one_by_id(self, id):
        """Remove an offer"""
        query = DatabaseQuery(self._db)
        record = query.delete("""
            DELETE FROM {table}
            WHERE id = %(id)s
            RETURNING id
        """.format(table=self._table), {'id': id}
        )

        return record[0] if record else None
