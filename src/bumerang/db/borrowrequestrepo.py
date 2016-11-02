from bumerang.db.databasequery import DatabaseQuery
from bumerang.error import InvalidIDConstraintError
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
        :return: The request specified by the id, or None if none found

        Throws InvalidIDConstraintError
        """
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT b0_.id, b0_.user_id, b0_.title, b0_.description, b0_.distance,
            b0_.duration, b0_.request_type FROM {table} b0_
            WHERE b0_.id = %(id)s
        """.format(table=self._table), {'id': id}
        )

        if len(records) > 1:
            raise InvalidIDConstraintError(id)

        if records:
            hydrator = Hydrator(records[0])
            return hydrator.to_borrow_request()
        else:
            return None

    def find_requests_by_user(self, user_id):
        """ Finds all requests created by user with the provided user id

        :user_id type: int
        :user_id: The id which identifies the user

        :rtype: list of BorrowRequest
        :return: A list of requests owned by the provided user, or None if none found

        Throws InvalidIDConstraintError
        """
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT b0_.id, b0_.user_id, b0_.title, b0_.description, b0_.distance,
            b0_.duration, b0_.request_type FROM {table} b0_
            WHERE b0_.user_id = %(user_id)s
        """.format(table=self._table), {'user_id': user_id}
        )
        
        if records:
            hydrators = [Hydrator(x) for x in records]
            return [x.to_borrow_request() for x in hydrators]
        else:
            return None


    def find_requests_by_recent(self, num_requests):
        """ Finds the most recently created requests

        :num_requests type: int
        :num_requests: The number of requests to fetch

        :rtype: list of BorrowRequest
        :return: A list of the most recent requests, or None if none found
        """
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT b0_.id, b0_.user_id, b0_.title, b0_.description, b0_.distance,
            b0_.duration, b0_.request_type FROM {table} b0_
            ORDER BY b0_.time_created DESC
            LIMIT %(num_requests)s
        """.format(table=self._table), {'num_requests': num_requests}
        )

        if records:
            hydrators = [Hydrator(x) for x in records]
            return [x.to_borrow_request() for x in hydrators]
        else:
            return None


    def insert_one(self, borrow_node):
        """Creates a new borrow_request

        :borrow_request type: BorrowRequest
        :borrow_request: The request that

        :return type: int
        :return: The id of the new request
        """
        query = DatabaseQuery(self._db)
        record = query.insert("""
            INSERT INTO {table} (TITLE, USER_ID, DESCRIPTION, DISTANCE, DURATION, REQUEST_TYPE)
            VALUES (%(title)s, %(user_id)s, %(description)s, %(distance)s, %(duration)s, %(request_type)s)
            RETURNING ID
        """.format(table=self._table), borrow_node
        )

        return record[0]
