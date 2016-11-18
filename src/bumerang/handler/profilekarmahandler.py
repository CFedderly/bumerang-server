from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler


class ProfileKarmaHandler(BumerangRequestHandler):

    def post(self, amount):
        id = self.get_arg('profile_id', required=True)
