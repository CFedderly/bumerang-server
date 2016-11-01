from bumerang.bumerangrequesthandler import BumerangRequestHandler
from bumerang.error import BumerangError


class OfferHandler(BumerangRequestHandler):

    def get(self, id):
        try:
            offer = self.offer_repo.find_one_by_id(id)
            if offer:
                node = offer.to_node()
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
        """Create a new offer"""
        offer = self._create_offer_node()
        try:
            offer_id = self.offer_repo.insert_one(offer)
            self.write({'id': offer_id})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def _create_offer_node(self):
        """Creates the offer from the request parameters

        :profile_id type: int
        :profile_id: The id of the user creating the request

        :borrow_id type: int
        :borrow_id: The id of the requst being responded to

        :rtype: dict
        :return: The node used to create the new offer"""
        return {
            'profile_id': self.get_arg('profile_id', required=True),
            'borrow_id': self.get_arg('borrow_id', required=True)
        }
