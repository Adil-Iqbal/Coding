import requests
from utility import *
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
            self.published = to_datetime.parse("1800-01-01T17:00:00.000Z")
            self.duration = None
            self.thumbnail = None
            self.curation = 0.0

    def __eq__(self, other):
        default = Content.__eq__(self, other)
        if default is False and type(other) is int:
            if self.episode_number == other:
                return True
            else:
                return self.uid == str(other)
        return default

    def from_dict(self, dictionary):
        """Assign dictionary values to class attributes."""
        Episode.validate_dictionary(dictionary)
        validate_ytid(dictionary["ytid"])
        super().from_dict(dictionary)

    def validate(self):
        """Ensure class meets criteria for propriety."""
        super().validate()
        validate_ytid(self.ytid)
        if self.type is not "episode":
            raise TypeError("{}: Content type must be \'episode\'. Was \'{}\')"
                            .format(self.uid, self.type))
        if type(self.episode_number) is not int or not self.episode_number > 0:
            raise TypeError('{}: Episode number must be an integer greater than 0. (Was type {} and value {})'
                            .format(self.uid, type(self.episode_number), self.episode_number))
        if not isinstance(self.published, datetime):
            raise TypeError('{}: Published attribute must be a datetime object. Was {}.'
                            .format(self.uid, type(self.published)))
        if type(self.thumbnail) is not str:
            raise TypeError('{}: Thumbnails attribute must be a string. Was {}.'
                            .format(self.uid, type(self.thumbnail)))
        if not self.title.startswith("Etho Plays Minecraft"):
            raise ValueError('{}: Episode title should start with \'Etho Plays Minecraft\'. Was {}.'
                             .format(self.uid, self.title))
        if type(self.duration) is not int or not self.duration > 0:
            raise ValueError('{}: Duration must be an integer greater than 0. Was type {} and value {}.'
                             .format(self.uid, type(self.duration), self.duration))
        if type(self.curation) is not float or not self.curation > 0 or not self.curation <= 100:
            raise ValueError('{}: Curation must be a float between 0 and 100. Was type {} and value {}.'
                             .format(self.uid, type(self.curation), self.curation))
        if self.episodes is not None:
            raise ValueError('{}: Episodes attribute must be None. Was {}'
                             .format(self.uid, self.episodes))

    @classmethod
    def request(cls, ytid):
        """Get new episode from the YouTube Data API."""
        validate_ytid(ytid)
        parameters = {
            "part": "snippet,contentDetails",
            "id": ytid,
            "key": "AIzaSyBoVWZevLKCgLn_v-KNyT7gt3fsr_JdA4M",
        }
        result = requests.request(method="get", url="https://www.googleapis.com/youtube/v3/videos", params=parameters)
        json_result = json.loads(result.text)
        new_episode = cls()
        new_episode.ytid = json_result['items'][0]['id']
        new_episode.title = json_result['items'][0]['snippet']['title']
        new_episode.episode_number = get_episode_num(json_result['items'][0]['snippet']['title'])
        new_episode.description = json_result['items'][0]['snippet']['description']
        new_episode.published = to_datetime.parse(json_result['items'][0]['snippet']['publishedAt'])
        new_episode.duration = convert_to_seconds(json_result['items'][0]['contentDetails']['duration'])
        new_episode.thumbnail = json_result['items'][0]['snippet']['thumbnails']['medium']['url']
        new_episode.validate()
        return new_episode
