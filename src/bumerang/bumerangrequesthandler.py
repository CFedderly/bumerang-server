from tornado.web import RequestHandler


class BumerangRequestHandler(RequestHandler):

    @property
    def borrow_repo(self):
        return self.application.borrow_repo
