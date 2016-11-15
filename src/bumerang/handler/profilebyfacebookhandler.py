from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler

class ProfileByFacebookHandler(BumerangRequestHandler):
    """ This class fetches a profile given a facebook id
    """

    def get(self, facebook_id):
        """Obtain a profile by facebook id.
        """
        try:
            profile = self.profile_repo.find_one_by_facebook_id(facebook_id)
            if profile:
                node = profile.to_node()
                self.write(node)
            else:
                self.set_status(404)
                self.finish(
                    {'error': 'A profile with id {} was not found'.format(facebook_id)}
                )
        except BumerangError as e:
            self.set_status(500)
            self.finish(
                {'error': str(e)}
            )
