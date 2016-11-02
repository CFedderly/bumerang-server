class BorrowRequest:

    def __init__(self, id, user_id, title, description, distance, duration, request_type):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.distance = distance
        self.duration = duration
        self.request_type = request_type;
        self.tags = set()

    def __eq__(self, other):
        return self.id == other.id and \
            self.user_id == other.user_id and \
            self.title == other.title and \
            self.description == other.description and \
            self.distance == other.distance and \
            self.duration == other.duration and \
            self.request_type == other.request_type and \
            self.tags == other.tags

    def __repr__(self):
        return 'BorrowRequest("{}", "{}", {}, {})'.format(
            self.title, self.description,
            self.distance, self.duration
        )

    # TODO add actual tag object
    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def to_node(self):
        """To serialize the object for a response"""
        return {
            'request': {
                'id': self.id,
                'user_id': self.user_id,
                'title': self.title,
                'description': self.description,
                'distance': self.distance,
                'duration': self.duration,
                'request_type': self.request_type,
                'tags': list(self.tags)
            }
        }


