class Profile:

    def __init__(
            self, id, facebook_id,
            device_id, first_name, last_name,
            description):
        """Create our profile object"""
        self.id = id,
        self.facebook_id = facebook_id,
        self.device_id = device_id,
        self.first_name = first_name,
        self.last_name = last_name,
        self.description = description
