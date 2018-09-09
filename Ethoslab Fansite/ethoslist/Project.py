from Content import Content
import dateutil.parser as to_datetime


class Project(Content):
    def __init__(self, source=None):
        Content.__init__(self, source)
        self.type = "project"
        if source is None:
            self.status = None
            self.begin_date = to_datetime.parse("9000-12-31T17:00:00.000Z")
            self.last_updated = to_datetime.parse("1800-01-01T17:00:00.000Z")
            self.season = None
            self.dimension = None
            self.x = None
            self.y = None
            self.z = None
            self.media = None
        self.validate()

    def validate(self):
        super().validate()
        self._validate_string_length()
        pass


raise NotImplementedError('Project class has not yet been implemented.')