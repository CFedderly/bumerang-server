class Profile:

    def __init__(
            self, id, facebook_id,
            device_id, first_name, last_name,
            description, phone_number, karma):
        """Create our profile object"""
        self.id = id
        self.facebook_id = facebook_id
        self.device_id = device_id
        self.first_name = first_name
        self.last_name = last_name
        self.description = description
        self.phone_number = phone_number
        self.karma = karma

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return 'Profile(%r, %r, %r, %r, %r, %r, %r, %r)' % (
            self.id, self.facebook_id, self.device_id,
            self.first_name, self.last_name, self.description,
            self.phone_number, self.karma
        )

    def to_node(self):
        """Serialize oject"""
        return {
            'profile': {
                'id': self.id,
                'facebook_id': self.facebook_id,
                'device_id': self.device_id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'description': self.description,
                'phone_number': self.phone_number,
                'karma': self.karma
            }
        }
