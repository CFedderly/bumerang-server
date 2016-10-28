from bumerang.error import InvalidQueryError

from psycopg2 import DatabaseError


class DatabaseQuery:
    """This class acts as an abtraction layer to interact with the database"""

    def __init__(self, db):
        self._db = db

    def create_table(self, query, parameters=None):
        """A query to abstraction to create tables in the db

        :query type: string
        :query: The query to create the table

        Throws InvalidQueryError
        """
        try:
            cur = self._db.cursor()
            self._mutator_query(query, parameters, cur)
            cur.close()

        except DatabaseError as e:
            if self._db:
                self._db.rollback()
            cur.close()
            raise InvalidQueryError(str(e))

    def insert(self, query, parameters=None):
        """A query abstraction to insert records into tables

        :query type: string
        :query: The query to insert the record

        :rtype: dict
        :return: A dictionary node of the created object

        Throws InvalidQueryError
        """
        try:
            cur = self._db.cursor()
            self._mutator_query(query, parameters, cur)
            result = cur.fetchone()
            cur.close()
            return result

        except DatabaseError as e:
            if self._db:
                self._db.rollback()

            cur.close()
            raise InvalidQueryError(str(e))

    def select(self, query, parameters=None):
        """Execute a query to fetch rows from a database.

        :query type: string
        :query: The query executed to fetch items from the database

        :rtype: TODO find out
        :return: All rows fetched from the database, unless an error occured,
        then return an empty list and log the error.
        """
        try:
            cur = self._db.cursor()
            cur.execute(query, parameters)
            result = cur.fetchall()
            cur.close()

            return result

        except DatabaseError as e:
            cur.close()
            raise InvalidQueryError(str(e))

    def _mutator_query(self, query, parameters, cur):
        """A wrapper around exec_query, which commits a change to the

           database.

        Throws DatabaseError
        """
        cur.execute(query, parameters)
        self._db.commit()
