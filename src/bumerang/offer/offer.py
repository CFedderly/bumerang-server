class Offer:

    def __init__(self, id, profile_id, borrow_id):
        #TODO change to profile and borrow
        self.id = id
        self.profile_id = profile_id
        self.borrow_id = borrow_id


    def __repr__(self):
        return 'Offer(%r, %r, %r)' % (
            self.id, self.profile_id,
            self.borrow_id
        )

    def __eq__(self, other):
        return self.id == other.id

    def to_node(self, profile_repo, borrow_repo):
        profile = profile_repo.find_one_by_id(self.profile_id)
        borrow = borrow_repo.find_one_by_id(self.borrow_id)
        return {
            'offer': {
                'id': self.id,
                'profile': profile.to_node(),
                'request': borrow.to_node()
            }
        }

    def fetch_device_id(self, profile_repo, borrow_repo):
        request = borrow_repo.find_one_by_id(self.borrow_id)
        profile = profile_repo.find_one_by_id(request.user_id)
        return profile.device_id
