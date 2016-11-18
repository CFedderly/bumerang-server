from bumerang.error import BumerangError
from bumerang.error import InvalidRequestTypeError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.notification.notification import Notification


class BorrowHandler(BumerangRequestHandler):
    """This class is here to handle any requests made by the user in attempt to
       borrow an item or something else that may be time sensitive.
    """
    Borrow = 0
    Lend = 1

    def get(self, id=None):
        """Obtain a request by id."""
        try:
            request = self.borrow_repo.find_one_by_id(id)
            if request:
                node = request.to_node()
                self.write(node)
            else:
                self.write_not_found(
                    'A request with id {} was not found'
                )
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def post(self):
        """Handle creating new requests and updating requests."""
        try:
            request = self._create_borrow_node()
            br_id, title = self.borrow_repo.insert_one(request)
            notification = Notification(title, '/topics/all', 0)
            self.noti_service.send_notification(notification)
            self.write({'id': br_id})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def delete(self, id):
        """Handle cancelling a request."""
        try:
            deleted_id = self.borrow_repo.remove_one_by_id(id)
            if deleted_id:
                self.write({'id': deleted_id})
            else:
                self.write_not_found(
                    'A request with id {} was not found'.format(id)
                )
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def _create_borrow_node(self):
        """Create the borrow request from the request parameters.

        :title type: str
        :title: The title of the request to be made

        :user_id type: int
        :user_id: The id of the user creating the request

        :description type: str
        :description: Additional details about the request

        :distance type: int
        :distance: The amount of meters that the request should use for match
            making

        :duration type: int
        :duration: The amount of minutes the request stays active for

        :request_type type: int
        :request_type: Is this request a borrow or a lend type.
        :rtype: dict
        :return: A dict with the parameters used to store the borrow request
            into the database
        """

        request_type = int(self.request.arguments['request_type'])
        if request_type not in [BorrowHandler.Borrow, BorrowHandler.Lend]:
            raise InvalidRequestTypeError(request_type)
        return {
            'title': self.get_arg('title', required=True),
            'user_id': self.get_arg('user_id', required=True),
            'description': self.get_arg('description', required=False),
            'distance': self.get_arg('distance', required=True),
            'duration': self.get_arg('duration', required=True),
            'request_type': request_type
        }
