from bumerang.health import HealthCheckHandler
from bumerang.profile import ProfileHandler

from tornado.ioloop import IOLoop
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line
from tornado.web import Application


define('debug', default=True, help='debug is on or not')
define('port', default=8888, help='run on given port', type=int)


def main():
    parse_command_line()
    app = Application(
        [
            (r'/health', HealthCheckHandler),
            (r'/profile/?', ProfileHandler),
            (r'/profile/([0-9]+)/?', ProfileHandler)
        ],
        debug=options.debug,
    )
    app.listen(options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
