from bumerang.error import BumerangError
from bumerang.error import InvalidOperationError
from bumerang.handler.bumerangrequesthandler import BumerangRequestHandler

from operator import add
from operator import sub


class ProfileKarmaHandler(BumerangRequestHandler):

    #TODO make enum
    METHODS = {'add', 'sub'}

    def post(self, id):
        """Add or remove karma"""
        try:
            amount = self.get_arg('amount', required=True)
            profile = self.profile_repo.find_one_by_id(id)
            if profile:
                operation = self._get_operation()
                profile.karma = operation(profile.karma, abs(amount))
                update_node = {'id': profile.id, 'karma': profile.karma}
                updated_id = self.profile_repo.update_karma(update_node)
                self.write({'id': updated_id})
            else:
                self.write_not_found(
                    'Profile with id {} not found'.format(id)
                )

        except BumerangError as e:
            self.set_status(500)
            self.finish({'error': str(e)})

    def _get_operation(self):
        method = self.get_arg('method', required=True)
        if method not in self.METHODS:
            raise InvalidOperationError(method)
        else:
            return add if method == 'add' else sub
