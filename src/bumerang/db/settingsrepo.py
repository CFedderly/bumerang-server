from bumerang.db.databasequery import DatabaseQuery
from bumerang.error import InvalidIDConstraintError
from bumerang.settings.hydrator import Hydrator


class SettingsRepo:

    def __init__(self, db, table):
        self._db = db
        self._table = table

    def __repr__(self):
        'SettingsRepo(%r)' % self._db

    def find_one_by_id(self, id):
        query = DatabaseQuery(self._db)
        records = query.select("""
            SELECT PROFILE_ID, REQUEST_NOTIFICATION, OFFER_NOTIFICATION
            FROM br_settings WHERE PROFILE_ID = %(id)s
        """.format(table=self._table), {'id': id}
        )

        if len(records) > 1:
            raise InvalidIDConstraintError(id)

        if records:
            hydrator = Hydrator(records[0])
            return hydrator.to_request()
        else:
            return None

    def edit_one(self, settings_node):
        """Edit existing settings for a profile"""
        query = DatabaseQuery(self._db)
        record = query.update("""
            UPDATE {table}
            SET REQUEST_NOTIFICATION = %(request_notification)s,
                OFFER_NOTIFICATION = %(offer_notification)s
            WHERE PROFILE_ID = %(profile_id)s
            RETURNING PROFILE_ID
        """.format(table=self._table), settings_node
        )
        return record[0]
