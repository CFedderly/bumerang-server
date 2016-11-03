class Offer:

    def __init__(self, id, profile_id, borrow_id):
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

    def to_node(self):
        return {
            'offer': {
                'id': self.id,
                'profile_id': self.profile_id,
                'borrow_id': self.borrow_id
            }
        }
