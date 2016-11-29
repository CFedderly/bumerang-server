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
        """Create the database

           Creates the database by first creating tables, the functions to be
           used by triggers, and then all triggers on the tables
        """
        self._create_tables()
        self._create_functions()
        self._create_triggers()

    def _create_tables(self):
        """Create all table schemas"""
        self._create_profile_table()
        self._create_settings_table()
        self._create_requests_table()
        self._create_offers_table()

    def _create_profile_table(self):
        """Create the table for the user profiles object"""
        query = DatabaseQuery(self._db)
        query.create_table("""
            CREATE TABLE IF NOT EXISTS br_profile(
                ID SERIAL PRIMARY KEY,
                FACEBOOK_ID BIGINT UNIQUE NOT NULL,
                DEVICE_ID VARCHAR (255) UNIQUE,
                FIRST_NAME VARCHAR (30) NOT NULL,
                LAST_NAME VARCHAR (30) NOT NULL,
                DESCRIPTION TEXT,
                PHONE_NUMBER VARCHAR (12) NOT NULL,
                KARMA INT DEFAULT 0
            )
        """)

    def _create_settings_table(self):
        """Create the table to store user settings"""
        query = DatabaseQuery(self._db)
        query.create_table("""
            CREATE TABLE IF NOT EXISTS br_settings(
                PROFILE_ID INT PRIMARY KEY REFERENCES br_profile(id),
                REQUEST_NOTIFICATION BOOLEAN DEFAULT 'false',
                OFFER_NOTIFICATION BOOLEAN DEFAULT 'true'
            )
        """)

    def _create_requests_table(self):
        """Create the table for the requests object"""
        query = DatabaseQuery(self._db)
        query.create_table("""
            CREATE TABLE IF NOT EXISTS br_request(
                ID SERIAL PRIMARY KEY,
                USER_ID INT REFERENCES br_profile(id) NOT NULL,
                TITLE VARCHAR (20) NOT NULL,
                DESCRIPTION TEXT,
                DISTANCE INT NOT NULL,
                DURATION INT NOT NULL,
                REQUEST_TYPE SMALLINT NOT NULL,
                TIME_CREATED TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
            )
        """)

    def _create_offers_table(self):
        """Create the table for holding the offers to fullfill a request"""
        query = DatabaseQuery(self._db)
        query.create_table("""
            CREATE TABLE IF NOT EXISTS br_offer(
                ID SERIAL PRIMARY KEY,
                PROFILE_ID INT REFERENCES br_profile NOT NULL,
                BORROW_ID INT NOT NULL REFERENCES br_request ON DELETE CASCADE,
                UNIQUE (PROFILE_ID, BORROW_ID)
            )
        """)

    def _create_functions(self):
        """Create the functions for the triggers to use"""
        self._create_settings_record_function()

    def _create_settings_record_function(self):
        """Have the function to insert new records into the db"""
        query = DatabaseQuery(self._db)
        query.create_function("""
            CREATE OR REPLACE FUNCTION settingsfunction()
            RETURNS TRIGGER AS $insert_settings_record$
                BEGIN
                    INSERT INTO br_settings (PROFILE_ID)
                    VALUES (new.id);
                    RETURN NEW;
                END;
            $insert_settings_record$ LANGUAGE plpgsql
        """)

    def _create_triggers(self):
        """Create the database triggers"""
        self._create_settings_record_trigger()

    def _create_settings_record_trigger(self):
        """On the creation of a profile account, create a settings record

           using the profile id.
        """
        query = DatabaseQuery(self._db)
        query.drop_trigger("""
            DROP TRIGGER IF EXISTS insert_settings_record on br_profile
        """)
        query.create_trigger("""
            CREATE TRIGGER insert_settings_record
            AFTER INSERT ON br_profile
            FOR EACH ROW EXECUTE PROCEDURE settingsfunction()
        """)
