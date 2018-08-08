from class_util import *
from Content import Content
from datetime import datetime
import dateutil.parser as to_datetime


class Episode(Content):
    def __init__(self, source=None):
        Content.__init__(self, source)
        self.type = "episode"
        self.episodes = None
        if source is None:
            self.ytid = None
            self.episode_number = None
            self.published = None
            self.duration = None
            self.thumbnails = None
            self.curation = None
        else:
            self.validate()

    def __eq__(self, other):
        default = Content.__eq__(self, other)
        if not default and type(other) is int:
            return self.episode_number == other
        else:
            return default

    def from_dict(self, dictionary):
        """Assign dictionary values to class attributes."""
        self._validate_dictionary(dictionary)
        Content.from_dict(self, dictionary)
        self.ytid = dictionary['ytid']
        self.episode_number = dictionary['episode_number']
        self.published = to_datetime.parse(dictionary['published'])
        self.duration = dictionary['duration']
        self.thumbnails = dictionary['thumbnails']
        self.curation = dictionary['curation']

    def validate(self):
        """Ensure class attributes have usable values."""
        self._base_validation()
        if self.type is not "episode":
            raise TypeError("{}: Object type is must be \'episode\'. Was \'{}\')".format(self.uid, self.type))
        validate_ytid(self.ytid)
        if type(self.episode_number) is not int or not self.episode_number > 0:
            raise TypeError('{}: Episode number must be an integer greater than 0. (Was type {} and value {})'
                            .format(self.uid, type(self.episode_number), self.episode_number))
        if not isinstance(self.published, datetime):
            raise TypeError('{}: Published attribute must be a datetime object. Was {}.'
                            .format(self.uid, type(self.published)))
        if type(self.duration) is not int or not self.duration > 0:
            raise ValueError('{}: Duration must be an integer greater than 0. Was type {} and value {}.'
                             .format(self.uid, type(self.duration), self.duration))
        if type(curation) is not float or not curation > 0 or not curation <= 100:
            raise ValueError('{}: Curation must be a float between 0 and 100. Was type {} and value {}.'
                             .format(self.uid, type(self.curation), self.curation))
        if type(self.thumbnails) is not dict:
            raise TypeError('{}: Thumbnails attribute must be a dictionary. Was {}.'
                            .format(self.uid, type(self.thumbnails)))

    def new(self, ytid):
        """Get new"""




a = Episode()
print(a.to_dict())