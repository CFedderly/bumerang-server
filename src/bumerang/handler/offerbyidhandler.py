from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.notification.notification import Notification
from json import dumps


class OfferByIdHandler(BumerangRequestHandler):

    def get(self, *ids):
        try:
            borrow_ids = [int(x) for x in ids[0].split(',')]
            all_offers = []
            for borrow_id in borrow_ids:
                offers = self.offer_repo.find_offers_by_borrow_id(borrow_id)
                if offers:
                    all_offers.extend(offers)

            if all_offers:
                nodes = [offer.to_node(self.profile_repo, self.borrow_repo) for offer in all_offers]
                json_string = dumps({'results': nodes})
                self.write(json_string)
            else:
                self.set_status(404)
                self.finish(
                    {
                        'error': (
                            'An offer with borrow id(s) {} was not found'
                        ).format(ids[0])
                    }
                )
        except ValueError as e:
            self.set_status(400)
            self.finish({'error': str(e)})
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})
