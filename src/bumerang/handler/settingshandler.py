from bumerang.error import BumerangError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler
from bumerang.settings.settings import Settings


class SettingsHandler(BumerangRequestHandler):

    def get(self, id):
        try:
            settings = self.settings_repo.find_one_by_id(id)
            if settings:
                self.write(settings.to_node())
            else:
                self.write_not_found(
                    "Setting wern't found with the id {}".format(id)
                )
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def post(self, id):
        try:
            settings = self.settings_repo.find_one_by_id(id)
            if settings:
                settings_edit_node = self._create_settings_edit_node()

                if any(settings_edit_node.values()):
                    settings_node = settings.to_node()['settings']
                    settings_node.update(settings_edit_node)
                    updated_id = self.settings_repo.edit_one(settings_node)
                    self.write({'id': updated_id})

                else:
                    self.set_status(400)
                    self.finish('Bad Request: No editable fields found')

            else:
                self.write_not_found(
                    'A profile with id {} was not found'.format(id)
                )
        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})


    def _create_settings_edit_node(self):
        """Create the settings node to store in the db"""
        return {
            'request_notification': self.get_arg(
                'request_notification', required=False
            ),
            'offer_notification': self.get_arg(
                'offer_notification', required=False
            )
        }
