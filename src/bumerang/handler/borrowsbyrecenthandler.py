from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.handler.bumerangrequesthandler import max_age_cache
from json import dumps


class BorrowsByRecentHandler(BumerangRequestHandler):
    """ This class handles fetching multiple bumerang requests depending
        on which are most recently created.
    """

    @max_age_cache(60)
    def get(self, num_requests=10):
        """Obtain a list of requests."""

        try:
            requests = self.borrow_repo.find_requests_by_recent(num_requests)
            if requests:
                nodes = [req.to_node() for req in requests]
                json_string = dumps({'results': nodes})
                self.write(json_string)
            else:
                self.set_status(404)
                self.finish(
                    {'error': 'A request with id {} was not found'.format(id)}
                )
        except ValueError as e:
            self.set_status(400)
            self.finish({'error': str(e)})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})
