from bumerang.db.borrowrequestrepo import BorrowRequestRepo
from bumerang.db.databasecreator import DatabaseCreator
from bumerang.db.offerrepo import OfferRepo
from bumerang.db.profilerepo import ProfileRepo
from bumerang.db.settingsrepo import SettingsRepo
from bumerang.handler.borrowsbyrecenthandler import BorrowsByRecentHandler
from bumerang.handler.borrowsbyuserhandler import BorrowsByUserHandler
from bumerang.handler.borrowhandler import BorrowHandler
from bumerang.handler.healthhandler import HealthCheckHandler
from bumerang.handler.profilekarmahandler import ProfileKarmaHandler
from bumerang.handler.offerbyidhandler import OfferByIdHandler
from bumerang.handler.offerbyuserhandler import OfferByUserHandler
from bumerang.handler.offerhandler import OfferHandler
from bumerang.handler.profilebyfacebookhandler import ProfileByFacebookHandler
from bumerang.handler.profileedithandler import ProfileEditHandler
from bumerang.handler.profilehandler import ProfileHandler
from bumerang.handler.settingshandler import SettingsHandler
from bumerang.notification.notificationservice import NotificationService

from os import environ

from psycopg2 import connect

from tornado.ioloop import IOLoop
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line
from tornado.web import Application

from urllib.parse import urlparse
from urllib.parse import uses_netloc


define('debug', default=True, help='debug is on or not')
define('test', default=False, help='running for tests or not')
define('port', default=8888, help='run on given port', type=int)


class BumerangApplication(Application):
    """This class serves as the base application for the API."""

    def __init__(self):
        """Set all endpoints and connect to the database."""
        handlers = [
            (r'/health/?', HealthCheckHandler),
            (r'/offer/?', OfferHandler),
            (r'/offer/([0-9]+)/?', OfferHandler),
            (r'/offer/user/([0-9]+)/?', OfferByUserHandler),
            (r'/offer/ids/([0-9]+(,[0-9]+)*)?/?', OfferByIdHandler),
            (r'/profile/?', ProfileHandler),
            (r'/profile/([0-9]+)/?', ProfileHandler),
            (r'/profile/edit/([0-9]+)/?', ProfileEditHandler),
            (r'/profile/facebookid/([0-9]+)/?', ProfileByFacebookHandler),
            (r'/profile/karma/edit/([0-9]+)/?', ProfileKarmaHandler),
            (r'/profile/settings/([0-9]+)/?', SettingsHandler),
            (r'/request/?', BorrowHandler),
            (r'/request/([0-9]+)/?', BorrowHandler),
            (r'/requests/recent/?', BorrowsByRecentHandler),
            (r'/requests/recent/([0-9]+)/?', BorrowsByRecentHandler),
            (r'/requests/user/([0-9]+)/?', BorrowsByUserHandler)
        ]
        settings = dict(debug=options.debug)
        self._db = self.connect_to_db() if not options.test else None
        if not options.test:
            self.set_repos(self._db)

        self.register_services()
        Application.__init__(self, handlers, **settings)

    def connect_to_db(self):
        """Connects to the database instance."""
        uses_netloc.append('postgres')
        url = urlparse(environ['DATABASE_URL'])

        conn = connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn

    def set_repos(self, db):
        """Set our repos for the use of the application.

           The purpose of these repos is to communicate with the tabels to
           obtain and store information instead of using the database
           connection directly.
        """
        creator = DatabaseCreator(self._db)
        creator()
        self.borrow_repo = BorrowRequestRepo(db, 'br_request')
        self.offer_repo = OfferRepo(db, 'br_offer')
        self.profile_repo = ProfileRepo(db, 'br_profile')
        self.settings_repo = SettingsRepo(db, 'br_settings')

    def register_services(self):
        """Register our serices for the application"""
        self.notification_service = NotificationService()


def main():
    parse_command_line()
    app = BumerangApplication()
    app.listen(options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
