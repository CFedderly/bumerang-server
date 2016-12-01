from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.error import BumerangError


class ProfileEditHandler(BumerangRequestHandler):
    """ Allows the user to edit their profile after it's created """

    def post(self, id):
        """ Update a profile's description, device id or phone number by id
            These are the only fields that are editable """
        try:
            profile = self.profile_repo.find_one_by_id(id)
            if profile:
                edit_node = self._create_edit_node()
                if not any(edit_node.values()):
                    self.set_status(400)
                    self.finish(
                        {'error':
                            (
                                'No editable field provided. '
                                'Profile with id {} not updated'
                            ).format(id)
                        }
                    )
                else:
                    profile_node = profile.to_node()['profile']
                    profile_node.update(edit_node)
                    profile_id = self.profile_repo.edit_one(profile_node)
                    self.write({'id': profile_id})

            else:
                self.write_not_found('A profile with id {} was not found'.format(id))
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def _create_edit_node(self):
        """ Create a node of attributes to update the profile with

        :rtype: dict
        :return: A node of attributes and the values they represent
        """
        edit_node = {}
        new_device_id = self.get_arg('device_id', required=False)
        if new_device_id:
            edit_node['device_id'] = new_device_id
        new_description = self.get_arg('description', required=False)
        if new_description:
            edit_node['description'] = new_description
        new_phone_number = self.get_arg('phone_number', required=False)
        if new_phone_number:
            edit_node['phone_number'] = new_phone_number

        return edit_node
