class Settings:
    """This class represents the settings for an individual user"""

    def __init__(self, id, request_notification, offer_notification):
        """Basic constructor for the settings object

        :id type: int
        :id: The id of the profile in which the settings correspong to

        :request_notification type: bool
        :request_notification: A boolean which represents whether a user will
            recieve notification when requests are create in which they are
            subscribed to or not

        :offer_notification type: bool
        :offer_notification: A boolean which represents whether a user will
            recieve a notification when requests are responded to or not.
        """
        self._profile_id = id
        self.req_noti = request_notification
        self.off_noti = offer_notification

    def __repr__(self):
        return 'Settings(%r, %r, %r)' \
            % (self._profile_id, self.req_noti, self.off_noti)

    def to_node(self):
        """Serialises the node to be returned to the user"""
        return {
            'settings': {
                'profile_id': self._profile_id,
                'request_notification': self.req_noti,
                'offer_notification': self.off_noti
            }
        }
