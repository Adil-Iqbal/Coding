from Content import Content


class Clip(Content):
    def __init__(self, source=None):
        Content.__init__(self, source)
        self.type = "clip"
        self.clips = None
        self.episodes = None
        if source is None:
            self.ytid = None
            self.published = None
            self.start = None
            self.end = None
        self.validate()

    def validate(self):
        super().validate()
        self._validate_string_length()
        pass


raise NotImplementedError('Clip class has not yet been implemented.')
