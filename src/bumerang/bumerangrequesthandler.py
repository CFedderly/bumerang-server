from bumerang.request.bumerangrequest import BumerangRequest
from tornado.web import RequestHandler


class BumerangRequestHandler(RequestHandler):
    """This class is here to handle and requests made by the user in attempt to
       borrow an item or something else that may be time sensitive.
    """

    def get(self, id=None):
        """Obtain a request by id."""
        request = BumerangRequest(
            'Macbook air charger', 'Please gimmi dat charge hype', 1, 3
        )

        if int(id) == request.id:
            self.write(repr(request))
        else:
            self.set_status(404)
            self.finish('A request with id {} was not found'.format(id))

    def post(self):
        """Handle creating new requests and updating requests."""
        request = self.create_bumerang_request()
        self.write(repr(request))

    def delete(self):
        """Handle cancelling a request."""
        self.write('Delete in requests')

    def create_bumerang_request(self):
        """Create the bumerang requests from the request parameters.

        :title type: str
        :title: The title of the request to be made

        :description type: str
        :description: Addtional details about the request

        :distance type: int
        :distance: The amount of meters that the request should use for match
            making

        :duration type: int
        :duration: The amount of minutes the request stays active for

        :rtype: BumerangRequest
        :return: A BumerangRequest object which represents a request created by
            the client
        """
        return BumerangRequest(
            title=self.get_argument('title'),
            description=self.get_argument('description', ''),
            distance=self.get_argument('distance'),
            duration=self.get_argument('duration')
        )
