from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.handler.bumerangrequesthandler import max_age_cache
from bumerang.error import BumerangError
from json import dumps


class BorrowsByUserHandler(BumerangRequestHandler):
    """ This class handles fetching multiple bumerang requests based on the user
        that created the request
    """

    @max_age_cache(60)
    def get(self, user_id):
        """Obtain a list of requests created by a given user."""

        try:
            user = int(user_id)
            requests = self.borrow_repo.find_requests_by_user(user)
            if requests:
                nodes = [req.to_node() for req in requests]
                json_string = dumps({'results': nodes})
                self.write(json_string)
            else:
                self.set_status(404)
                self.finish(
                    {
                        'error': (
                            'A request from user with id {} was not found'
                        ).format(user_id)
                    }
                )
        except ValueError as e:
            self.set_status(400)
            self.finish({'error': str(e)})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})
