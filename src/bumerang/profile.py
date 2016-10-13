from tornado.escape import json_decode
from tornado.web import RequestHandler

default_profile = {
    'firstname': 'John',
    'lastname': 'Doe',
    'description': 'I like pina coladas and getting caught in the rain',
    'tags': 'pina coladas, rain'
}


class ProfileHandler(RequestHandler):

    def get(self, id=None):
        """ Included a get for a profile with an id in case we want to

            eventually look at another user's profile.
        """
        if id is not None:
            self.write(id + " Get profile")
        else:
            self.write(default_profile)

    def post(self):
        parsed_json = json_decode(self.request.body)
        self.write(parsed_json)
