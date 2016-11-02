from bumerang.db.databasequery import DatabaseQuery


class DatabaseCreator:
    """The purpose of this class is to create all tables for the database on

       startup, in case one gets dropped or it's the initial run of the
       application.
    """

    def __init__(self, db):
        self._db = db

    def __call__(self):
        """Allow the DatabaseCreator to be called functionally."""
        self.create_database()

    def create_database(self):
        """Create all database schemas."""
        self._create_profile_table()
        self._create_requests_table()
        self._create_tags_table()

    def _create_profile_table(self):
        """Create the table for the user profiles object"""
        query = DatabaseQuery(self._db)
        query.create_table("""
            CREATE TABLE IF NOT EXISTS br_profile(
                ID SERIAL PRIMARY KEY,
                FACEBOOK_ID BIGINT UNIQUE NOT NULL,
                DEVICE_ID BIGINT UNIQUE,
                FIRST_NAME VARCHAR (30) NOT NULL,
                LAST_NAME VARCHAR (30) NOT NULL,
                DESCRIPTION TEXT
            )
        """)

    def _create_requests_table(self):
        """Create the table for the requests object

            TODO: Add error handling
        """
        query = DatabaseQuery(self._db)
        query.create_table("""
            CREATE TABLE IF NOT EXISTS br_request(
                ID SERIAL PRIMARY KEY,
                TITLE VARCHAR (20) NOT NULL,
                DESCRIPTION VARCHAR (200),
                DISTANCE INT,
                DURATION INT
            )
        """)

    def _create_tags_table(self):
        """Create the table to hold all the tags"""
        pass
