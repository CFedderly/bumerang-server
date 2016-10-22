from bumerang.borrowhandler import BorrowHandler
from bumerang.db.borrowrequestrepo import BorrowRequestRepo
from bumerang.db.databasecreator import DatabaseCreator
from bumerang.healthhandler import HealthCheckHandler
from bumerang.profilehandler import ProfileHandler

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
            (r'/profile/?', ProfileHandler),
            (r'/profile/([0-9]+)/?', ProfileHandler),
            (r'/request/?', BorrowHandler),
            (r'/request/([0-9]+)/?', BorrowHandler),
        ]
        settings = dict(debug=options.debug)
        self._db = self.connect_to_db() if not options.test else None
        if not options.test:
            creator = DatabaseCreator(self._db)
            creator()
            self.set_repos(self._db)

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
        self.borrow_repo = BorrowRequestRepo(db, 'br_requests')


def main():
    parse_command_line()
    app = BumerangApplication()
    app.listen(options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
