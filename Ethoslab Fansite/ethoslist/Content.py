from utility import *
from pprint import pprint
from datetime import datetime
from abc import ABC, abstractmethod
from operator import attrgetter


class Content(ABC):
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
            raise TypeError('{}: Source must be a string, dictionary, object class, or None. Was {}'
                            .format(self.uid, type(source)))

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

    def __repr__(self):
        def force_string_length(string, length, filler=" "):
            string = str(string)
            length = int(length)
            while len(string) < length:
                string += filler
            return string[:length]

        a = self.type[0].upper() if self.type is not None else 'N'
        b = self.uid
        x = 31 if a is 'E' else 0
        y = str(self.title)
        c = force_string_length(y[x:], 20)
        d = force_string_length(self.description, 30)

        return f'{a}-{b} #{c} #{d}'

    def to_dict(self):
        """Convert instance into a dictionary and return it."""
        dictionary = {}
        for attribute, value in self.__dict__.items():
            if isinstance(value, datetime):
                dictionary[attribute] = value.isoformat()
            else:
                dictionary[attribute] = value
        return dictionary

    def from_dict(self, dictionary):
        """Assign dictionary values to class attributes."""
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])
        # self.uid = dictionary['uid']
        # self.type = dictionary['type']
        # self.title = dictionary['title']
        # self.description = dictionary['description']
        # self.clips = dictionary['clips']
        # self.episodes = dictionary['episodes']
        # self.projects = dictionary['projects']


    @classmethod
    def validate_dictionary(cls, dictionary):
        """Ensure dictionary is compatible with this class."""
        class_instance = cls()
        if type(dictionary) is not dict:
            raise TypeError('{}: This function expects a dictionary.'.format(class_instance.uid))
        dictionary_keys = dictionary.keys()
        attributes = []
        for attribute, value in class_instance.__dict__.items():
            attributes.append(attribute)
        for index, key in enumerate(dictionary_keys):
            if key not in attributes:
                raise KeyError('{}: Dictionary contains unexpected key: {}'.format(class_instance.uid, key))
        for index, attribute in enumerate(attributes):
            if attribute not in dictionary_keys:
                raise KeyError('{}: Dictionary is missing a required key: {}'.format(class_instance.uid, attribute))
        validate_uid(dictionary['uid'])
        validate_content_type(dictionary['type'])
        if dictionary['type'] is not class_instance.type:
            raise TypeError('{}: Object type of dictionary ({}) does not match object type of class ({}).'
                            .format(class_instance.uid, dictionary['type'], class_instance.type))

        def cep_validation(key_, data):
            """Ensure linking lists are the correct type."""
            if type(data) is not list and data is not None:
                raise TypeError('{}: A linking list in this dictionary was neither a list nor None. Was type {}.'
                                .format(class_instance.uid, dictionary[key_]))
            elif data is not None:
                validate_uid_list(data)

        cep_validation('clips', dictionary['clips'])
        cep_validation('episodes', dictionary['episodes'])
        cep_validation('projects', dictionary['projects'])
        if class_instance.type in ('clip', 'episode') and dictionary['episodes'] is not None:
            raise ValueError('{}: A dictionary of content type {} should not have an episodes list.'
                             .format(class_instance.uid, class_instance.type))
        if class_instance.type is 'clip' and dictionary['clips'] is not None:
            raise ValueError('{}: A dictionary of content type {} should not have a clips list.'
                             .format(class_instance.uid, class_instance.type))

    @abstractmethod
    def validate(self):
        raise NotImplementedError('Method to be overridden by child classes.')

    def load(self, uid):
        """Overwrite this instance with a saved dictionary."""
        validate_uid(uid)
        dictionary = retrieve_dictionary_by_uid(uid, self.type)
        self.from_dict(dictionary)

    def save(self):
        """Save instance into appropriate JSON file."""
        self._curate()
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
        if self.clips is None:
            raise AttributeError('{} {}: This parent method has been disabled.'.format(self.type[:2].upper(), self.uid))
        return Content._batch_load_classes_from_uids(self.clips, 'clip')

    def get_episodes(self):
        """Return list of classes representing associated episodes."""
        if self.episodes is None:
            raise AttributeError('{} {}: This parent method has been disabled.'.format(self.type[:2].upper(), self.uid))
        return Content._batch_load_classes_from_uids(self.episodes, 'episode')

    def get_projects(self):
        """Return list of classes representing associated projects."""
        if self.projects is None:
            raise AttributeError('{} {}: This parent method has been disabled.'.format(self.type[:2].upper(), self.uid))
        return Content._batch_load_classes_from_uids(self.projects, 'project')

    def print(self):
        pprint(self.to_dict())

    def _base_class_validation(self):
        """Ensure base attributes meet criteria for propriety. (PRIVATE)"""
        validate_uid(self.uid)
        validate_content_type(self.type)
        if type(self.title) is not str:
            raise TypeError('{}: Title attribute must be a string. Was type {}.'.format(self.uid, type(self.title)))
        if type(self.description) is not str:
            raise TypeError('{}: Description attribute must be a string. Was type {}.'
                            .format(self.uid, type(self.description)))
        if self.type is not "episode":
            title_length = len(self.title)
            description_length = len(self.description)
            if not title_length > 0 or not title_length <= 50:
                raise ValueError('{}: Title must have a length between 1 - 50. Was length {} with value: {}'
                                 .format(self.uid, title_length, self.title))
            if not description_length > 0 or not description_length <= 140:
                raise ValueError('{}: Description must have length between 1 - 140. Was length {} with value: {}'
                                 .format(self.uid, description_length, self.description))
        if self.clips is not None:
            validate_uid_list(self.clips)
        if self.episodes is not None:
            validate_uid_list(self.episodes)
        if self.projects is not None:
            validate_uid_list(self.projects)

    def _curate(self, content_type=None):
        """Curate associated clips, episodes, and projects by date/time where applicable. (PRIVATE)"""
        if self.clips is not None and content_type in ('clip', None):
            temp = self.get_clips()
            temp.sort(key=attrgetter('published', 'start'))
            self.clips = list_to_uids(temp)
        if self.episodes is not None and content_type in ('episode', None):
            temp = self.get_episodes()
            temp.sort(key=attrgetter('published'))
            self.episodes = list_to_uids(temp)
        if self.projects is not None and content_type in ('project', None):
            temp = self.get_projects()
            temp.sort(key=attrgetter('begin_date'))
            self.projects = list_to_uids(temp)

    @staticmethod
    def _batch_load_classes_from_uids(source_list, content_type=None):
        """Turn entire list of UID into classes all at once. (PRIVATE)"""
        validate_uid_list(source_list)
        classes = []
        if content_type is None:
            data = access_all_dictionaries()
        else:
            validate_content_type(content_type)
            data = access_dictionary(content_type)
        for index, content in enumerate(data):
            if content['uid'] in source_list:
                classes.append(any_to_class(content))
                if len(source_list) > 1:
                    source_list.remove(content['uid'])
                else:
                    break
        return classes
