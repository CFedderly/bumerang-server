from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler


class ProfileHandler(BumerangRequestHandler):

    def get(self, id):
        """Obtain a profile by id."""
        try:
            profile = self.profile_repo.find_one_by_id(id)
            if profile:
                node = profile.to_node()
                self.write(node)
            else:
                self.write_not_found('A profile with id {} was not found'.format(id))
        except BumerangError as e:
            self.set_status(500)
            self.finish(
                {'error': str(e)}
            )

    def post(self):
        """Create a profile"""
        try:
            profile = self._create_profile_node()
            profile_id = self.profile_repo.insert_one(profile)
            if profile_id:
                self.write({'id': profile_id})

        except BumerangError as e:
            self.set_status(500)
            self.finish(
                {'error': str(e)}
            )

    def _create_profile_node(self):
        """Create the profile from the request parameters.

        :facebook_id type: numeric_str
        :facebook_id: The id given by facebook for a given user's facebook
            account

        :device_id type: numeric_str
        :device_id: The device id provided by Android, used for notifications

        :first_name type: str
        :first_name: The first name of the user

        :last_name type: str
        :last_name: The last name of the user

        :description type: str
        :description: Some text about the user

        :phone_number type: str
        :phone_number: The user's phone number

        :rtype: dict
        :return: A request used to create the profile
        """
        return {
            'facebook_id': self.get_arg('facebook_id', required=True),
            'device_id': self.get_arg('device_id', required=False),
            'first_name': self.get_arg('first_name', required=True),
            'last_name': self.get_arg('last_name', required=True),
            'description': self.get_arg('description', required=False),
            'phone_number': self.get_arg('phone_number', required=True)
        }
