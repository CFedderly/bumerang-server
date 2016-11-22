from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.notification.notification import Notification


class OfferHandler(BumerangRequestHandler):

    def get(self, id):
        try:
            offer = self.offer_repo.find_one_by_id(id)
            if offer:
                node = offer.to_node(self.profile_repo, self.borrow_repo)
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
            #TODO clean up logic probs by join
            offer = self.offer_repo.find_one_by_id(offer_id)
            profile = offer.fetch_profile(
                self.profile_repo,
                self.borrow_repo
            )
            self._send_notification(profile)
            self.write({'id': offer_id})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def delete(self, offer_id):
        """Delete an offer"""
        try:
            deleted_id = self.offer_repo.remove_one_by_id(offer_id)
            if deleted_id:
                self.write({'id': deleted_id})
            else:
                self.write_not_found(
                    'Offer with id {id} was not found.'.format(id=deleted_id)
                )
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

    def _send_notification(self, profile):
        """Sends a notificaiton when an offer is created"""
        settings = self.settings_repo.find_one_by_id(profile.id)
        print(settings)
        if settings.off_noti:
            noti = Notification('You have an offer!', profile.device_id, 1)
            self.noti_service.send_notification(noti)
