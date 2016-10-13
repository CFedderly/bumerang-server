class BumerangRequest:

    def __init__(self, title, description, distance, duration):
        self.id = 1
        self.title = title
        self.description = description
        self.distance = distance
        self.duration = duration
        self.tags = set()

    def __repr__(self):
        return 'BumerangRequest("{}", "{}", {}, {})'.format(
            self.title, self.description,
            self.distance, self.duration
        )

    # TODO add actual tag object
    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)
