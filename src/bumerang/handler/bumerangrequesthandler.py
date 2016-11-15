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
    def noti_service(self):
        return self.application.notification_service

    def get_arg(self, name, required=False):
        """Get a given argument from a request"""
        if not required:
            return self.request.arguments.get(name, None)
        else:
            return self.request.arguments[name]
