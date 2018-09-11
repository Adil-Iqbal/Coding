from utility import *
from Content import Content
from Episode import Episode
from datetime import datetime
import dateutil.parser as to_datetime


class Clip(Content):
    def __init__(self, source=None):
        Content.__init__(self, source)
        self.type = "clip"
        self.clips = None
        self.episodes = None
        if source is None:
            self.parent = None
            self.ytid = None
            self.published = to_datetime.parse("1800-01-01T17:00:00.000Z")
            self.start = 0
            self.end = 2160000

    def validate(self):
        """Ensure class meets criteria for propriety."""
        super().validate()
        self._validate_string_length()
        validate_ytid(self.ytid)
        validate_uid(self.parent)
        if self.type is not "clip":
            raise TypeError("{}: Content type must be \'clip\'. Was \'{}\')"
                            .format(self.uid, self.type))
        if not isinstance(self.published, datetime):
            raise TypeError('{}: Published attribute must be a datetime object. Was {}.'
                            .format(self.uid, type(self.published)))
        if type(self.start) is not int:
            raise TypeError('{}: Start attribute must be of type integer. Was {}'
                            .format(self.uid, type(self.start)))
        if type(self.end) is not int:
            raise TypeError('{}: End attribute must be of type integer. Was {}'
                            .format(self.uid, type(self.end)))
        if self.clips is not None:
            raise ValueError('{}: Clips attribute must be None. Was {}'
                             .format(self.uid, self.clips))
        if self.episodes is not None:
            raise ValueError('{}: Episodes attribute must be None. Was {}'
                             .format(self.uid, self.episodes))
        if not self.start >= 0:
            raise ValueError('{}: Start attribute must greater than or equal to zero. Was {}'
                             .format(self.uid, self.start))
        if not self.end >= 0:
            raise ValueError('{}: End attribute must greater than or equal to zero. Was {}'
                             .format(self.uid, self.end))
        if self.end <= self.start:
            raise ValueError('{}: End attribute must be greater than start attribute. Start was {}. End was {}.'
                             .format(self.uid, self.start, self.end))

    def set_parent(self, uid):
        """Set parent episode for this clip."""
        validate_uid(uid)
        if uid == self.parent:
            return

        new_parent = Episode(uid)
        old_parent = Episode(self.parent)

        self.parent = new_parent.uid
        self.ytid = new_parent.ytid
        self.published = new_parent.published

        old_parent.clips.remove(self.uid)
        new_parent.clips.append(self.uid)

        old_parent.save()
        new_parent.save()
        self.save()
