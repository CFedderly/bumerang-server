from bumerang.error import InvalidArgumentError
from tornado.web import RequestHandler
from tornado.escape import json_decode


class BumerangRequestHandler(RequestHandler):

    def prepare(self):
        if self.request.body:
            try:
                json_data = json_decode(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON object'
                self.send_error(400, message=message)

    @property
    def borrow_repo(self):
        return self.application.borrow_repo

    @property
    def offer_repo(self):
        return self.application.offer_repo

    @property
    def profile_repo(self):
        return self.application.profile_repo

    @property
    def settings_repo(self):
        return self.application.settings_repo

    @property
    def noti_service(self):
        return self.application.notification_service

    def get_arg(self, name, required=False):
        """Get a given argument from a request

        :type name: str
        :name: The name of the argument to check in the request

        :type required: bool
        :required: Whether the argument is required or not

        :rtype: Mixed
        :return: The value of the argument from the request parameters. Must
            conform to JSON

        Raises InvalidArgumentError
        """
        if not required:
            return self.request.arguments.get(name, None)
        else:
            try:
                return self.request.arguments[name]
            except KeyError:
                raise InvalidArgumentError(name)

    def write_not_found(self, msg):
        self.set_status(404)
        self.write({'error': msg})
