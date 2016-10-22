from bumerang.db.databasequery import DatabaseQuery
from bumerang.request.hydrator import Hydrator


class BorrowRequestRepo:

    def __init__(self, db, table):
        self._db = db
        self._table = table

    def find_one_by_id(self, id):
        """Finds a borrow request by it's id.

        :id type: int
        :id: The id which identifies the request

        :rtype: BorrowRequest
        :return: The request specified by the id, or None if none found"""
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT b0_.id, b0_.title, b0_.description, b0_.distance,
            b0_.duration FROM {table} b0_
            WHERE b0_.id = %(id)s
        """.format(table=self._table), {'id': id}
        )
        assert len(records) == 1, (
            'ids must be unique, more then one record'
            'with with an id of {id}'
            ).format(id=id)

        hydrator = Hydrator(records[0])
        return hydrator.to_borrow_request()

    def insert_one(self, borrow_node):
        """Creates a new borrow_request

        :borrow_request type: BorrowRequest
        :borrow_request: The request that

        :return type: int
        :return: The id of the new request
        """
        query = DatabaseQuery(self._db)
        record = query.insert("""
            INSERT INTO {table} (title, description, distance, duration)
            VALUES (%(title)s, %(description)s, %(distance)s, %(duration)s)
            RETURNING id
        """.format(table=self._table), borrow_node
        )

        return record[0]
