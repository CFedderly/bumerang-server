from bumerang.bumerangrequesthandler import BumerangRequestHandler
from bumerang.error import BumerangError


class BorrowHandler(BumerangRequestHandler):
    """This class is here to handle and requests made by the user in attempt to
       borrow an item or something else that may be time sensitive.
    """

    def get(self, id=None):
        """Obtain a request by id."""
        try:
            request = self.borrow_repo.find_one_by_id(id)
            if request:
                node = request.to_node()
                self.write(node)
            else:
                self.set_status(404)
                self.finish(
                    {'error': 'A request with id {} was not found'.format(id)}
                )
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def post(self):
        """Handle creating new requests and updating requests."""
        request = self._create_borrow_node()
        try:
            br_id = self.borrow_repo.insert_one(request)
            self.write({'id': br_id})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def delete(self):
        """Handle cancelling a request."""
        self.write('delete not implemented')

    def _create_borrow_node(self):
        """Create the borrow request from the request parameters.

        :title type: str
        :title: The title of the request to be made

        :description type: str
        :description: Addtional details about the request

        :distance type: int
        :distance: The amount of meters that the request should use for match
            making

        :duration type: int
        :duration: The amount of minutes the request stays active for

        :rtype: dict
        :return: A dict with the parameters used to store the borrow request
            into the database
        """
        return {
            'title': self.get_argument('title'),
            'description': self.get_argument('description', ''),
            'distance': self.get_argument('distance'),
            'duration': self.get_argument('duration')
        }
