from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.notification.notification import Notification
from json import dumps


class OfferByUserHandler(BumerangRequestHandler):

    def get(self, user_id):
        try:
            offers = self.offer_repo.find_offers_by_user_id(user_id)
            if offers:
                nodes = [offer.to_node(self.profile_repo, self.borrow_repo) for offer in offers]
                json_string = dumps({'results': nodes})
                self.write(json_string)
            else:
                self.write_not_found('An offer with user id {} was not found'.format(user_id))
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})