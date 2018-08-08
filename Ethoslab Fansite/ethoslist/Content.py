from class_util import *
from abc import ABCMeta, abstractmethod


class Content(object):
    __metaclass__ = ABCMeta

    def __init__(self, source=None):
        if source is None:
            self.uid = generate_uid()
            while not is_unique(self.uid):
                self.uid = generate_uid()
            self.type = None
            self.title = None
            self.description = None
            self.clips = []
            self.episodes = []
            self.projects = []
        elif type(source) is dict:
            self.from_dict(source)
        elif isinstance(source, Content):
            self.from_dict(source.to_dict())
        elif type(source) is str:
            self.load(source)
        else:
            raise TypeError(
                f'{self.uid}: Source must be a string, dictionary, object class, or None. (Was {type(source)})')

    def __eq__(self, other):
        if type(other) in (float, list):
            return False
        elif type(other) is int and self.type is not 'episode':
            return self.uid == str(int)
        elif type(other) is str:
            return self.uid == other
        elif type(other) is dict and 'uid' in other.keys():
            return self.uid == other['uid']
        elif isinstance(other, Content):
            return self.uid == other.uid
        else:
            return False

    def to_dict(self):
        """Convert instance into a dictionary and return it."""
        dictionary = {}
        for attribute, value in self.__dict__.items():
            dictionary[attribute] = value
        return dictionary

    def _validate_dictionary(self, dictionary):
        """Ensure dictionary is compatible with this class."""
        if type(dictionary) is not dict:
            raise TypeError('{}: This function expects a dictionary.'.format(self.uid))
        dictionary_keys = dictionary.keys()
        attributes = []
        for attribute, value in self.__dict__.items():
            attributes.append(attribute)
        for index, key in enumerate(dictionary_keys):
            if key not in attributes:
                raise KeyError('{}: Dictionary contains unexpected key: {}'.format(self.uid, key))
        for index, attribute in enumerate(attributes):
            if attribute not in dictionary_keys:
                raise KeyError('{}: Dictionary is missing a required key: {}'.format(self.uid, attribute))
        if dictionary['type'] is not self.type:
                raise TypeError('{}: Object type of dictionary ({}) does not match object type of class ({}).'
                                .format(self.uid, dictionary['type'], self.type))

    def from_dict(self, dictionary):
        """Assign dictionary values to class attributes."""
        self.uid = dictionary['uid']
        self.type = dictionary['type']
        self.title = dictionary['title']
        self.description = dictionary['description']
        self.clips = dictionary['clips']
        self.episodes = dictionary['episodes']
        self.projects = dictionary['projects']

    @abstractmethod
    def validate(self):
        raise NotImplementedError('Method to be overridden by child classes.')

    def _base_validation(self):
        """Ensure base attributes meet criteria for propriety."""
        validate_uid(self.uid)
        validate_type(self.type)
        if self.type is not "episode":
            title_length = len(self.title)
            description_length = len(self.description)
            if type(self.title) is not str or not title_length > 0 or not title_length <= 50:
                raise ValueError('{}: Title must be a string with length between 1 - 50. '
                                 'Was type {}, length {}, value: {}'
                                 .format(self.uid, type(self.title), title_length, self.title))
            if type(self.description) is not str or not description_length > 0 or not description_length <= 140:
                raise ValueError('{}: Description must be a string with length between 1 - 140. '
                                 'Was type {}, length {}, value: {}'
                                 .format(self.uid, type(self.description), description_length, self.description))
        if self.clips is not None:
            validate_uid_list(self.clips)
        if self.episodes is not None:
            validate_uid_list(self.episodes)
        if self.projects is not None:
            validate_uid_list(self.projects)

    def load(self, uid):
        """Overwrite this instance with a saved dictionary."""
        validate_uid(uid)
        dictionary = retrieve_dictionary_by_uid(uid, self.type)
        self.from_dict(dictionary)

    def save(self):
        """Save instance into appropriate JSON file."""
        self.validate()
        data = access_dictionary(self.type)
        to_append = True
        for index, content in enumerate(data):
            if self.uid == content['uid']:
                data[index] = self.to_dict()
                to_append = False
        if to_append:
            data.append(self.to_dict())
        update_file(self.type, data)

    def get_clips(self):
        """Return list of classes representing associated clips."""
        if self.clips is not None:
            from editor_util import list_of_uids_to_classes
            return list_of_uids_to_classes(self.clips)

    def get_episodes(self):
        """Return list of classes representing associated episodes."""
        if self.episodes is not None:
            from editor_util import list_of_uids_to_classes
            return list_of_uids_to_classes(self.episodes)
        else:
            AttributeError('{} {}: This parent method has been disabled.'.format(self.type[:2].upper(), self.uid))

    def get_projects(self):
        """Return list of classes representing associated projects."""
        if self.projects is not None:
            from editor_util import list_of_uids_to_classes
            return list_of_uids_to_classes(self.projects)


a = Content()
print(a.to_dict())
print(type(a))