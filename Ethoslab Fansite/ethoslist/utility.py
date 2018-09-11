import os
import sys
import json
import traceback
from random import randint

"""Utility function for Ethoslist Classes"""


def validate_list(list_):
    if type(list_) is not list:
        raise TypeError('This function expects a list.')


def validate_content_type(string):
    """Ensure that string represents a usable object type."""
    if string not in ('clip', 'episode', 'project'):
        raise TypeError("Parameter must equal \'clip\', \'project\', or \'episode.\'")


def validate_uid(string):
    """Ensure that the string represents a valid UID."""
    if type(string) is not str or len(string) is not 5 or not string.isalnum():
        raise TypeError('{} is not a valid UID.'.format(string))


def validate_uid_list(list_):
    """Ensure that all UIDs in a list are a valid UID."""
    validate_list(list_)
    for index, uid in enumerate(list_):
        validate_uid(uid)


def validate_ytid(string):
    """Ensure that the string represents a valid YouTube ID."""
    error_message = '{} is not a valid YTID.'.format(string)
    if type(string) is not str and len(string) is not 11:
        raise TypeError(error_message)
    for char in string:
        if not char.isalnum() and char is not "-" and char is not "_":
            raise TypeError(error_message)


def validate_dict(dictionary):
    """Ensure that a dictionary is a valid."""
    if type(dictionary) is not dict:
        raise TypeError('This function expects a dictionary')
    if 'type' not in dictionary.keys():
        raise KeyError('This dictionary does not have a \'type\' key.')
    validate_content_type(dictionary['type'])
    if dictionary['type'] is 'episode':
        from Episode import Episode
        Episode.validate_dictionary(dictionary)
    elif dictionary['type'] is 'clip':
        from Clip import Clip
        Clip.validate_dictionary(dictionary)
    elif dictionary['type'] is 'project':
        from Project import Project
        Project.validate_dictionary(dictionary)


def generate_uid(len_=5):
    """Generate and return a UID."""
    characters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    uid = ''
    for i in range(len_):
        roll = randint(0, len(characters)-1)
        uid += characters[roll]
    validate_uid(uid)
    return uid


def is_unique(uid):
    """Return boolean expressing whether UID is unique."""
    validate_uid(uid)
    data = access_all_dictionaries()
    for content in data:
        if uid == content.uid:
            return False
    return True


def path_to(type_):
    """Convert relative path to absolute path."""
    validate_content_type(type_)
    relative_path = 'data/' + type_ + 's.json'
    absolute_path = os.path.dirname(__file__)
    return os.path.join(absolute_path, relative_path)


def access_dictionary(type_):
    """Access and return specific JSON file as an array of dictionaries."""
    validate_content_type(type_)
    file_path = path_to(type_)
    with open(file_path, "r") as json_data:
        dict_data = json.load(json_data)
        return dict_data


def access_all_dictionaries():
    """Access and return all JSON files as an array of dictionaries."""
    c_data = access_dictionary('clip')
    e_data = access_dictionary('episode')
    p_data = access_dictionary('project')
    return c_data + e_data + p_data


def determine_content_type(data):
    """Determine object type of data and return it as a string."""
    from Content import Content
    if type(data) is str:
        validate_uid(data)
        data = retrieve_dictionary_by_uid(data)
        return determine_content_type(data)
    elif type(data) is dict:
        validate_content_type(data['type'])
        return data['type']
    elif isinstance(data, Content):
        validate_content_type(data.type)
        return data.type
    else:
        raise TypeError('Can only check type of a uid, dictionary, or class.')


def validate_list_uniformity(data, type_=None):
    """Ensure that all elements of a list are of the same data type and content type."""
    validate_list(data)
    data_type = type(data[0])
    if type_ is not None:
        validate_content_type(type_)
        content_type = type_
    else:
        content_type = determine_content_type(data)
    for index, value in enumerate(data):
        if not type(value) == data_type:
            raise TypeError('List contains different data types.')
        if not determine_content_type(value) == content_type:
            raise TypeError('List contains different content types.')


def update_file(type_, data):
    """Save modified list of dictionaries to the corresponding JSON file."""
    validate_content_type(type_)
    validate_list_uniformity(data, type_)
    file_path = path_to(type_)
    with open(file_path, "w") as json_data:
        json.dump(data, json_data)


def retrieve_dictionary_by_uid(uid, content_type=None):
    """Return dictionary with matching uid."""
    validate_uid(uid)
    if content_type is not None:
        validate_content_type(content_type)
        data = access_dictionary(content_type)
    else:
        data = access_all_dictionaries()
    for index, dictionary in enumerate(data):
        if dictionary['uid'] == uid:
            return dictionary
    raise FileNotFoundError('Dictionary of type \'{}\' with id \'{}\' was not found.'.format(content_type, uid))


def retrieve_list_of_dictionaries_by_uid(source_list, type_=None):
    """Return list of dictionaries corresponding to UIDs in list."""
    validate_uid_list(source_list)
    dictionaries = []
    if type_ is None:
        data = access_all_dictionaries()
    else:
        validate_content_type(type_)
        data = access_dictionary(type_)
    for index, content in enumerate(data):
        if content['uid'] in source_list:
            dictionaries.append(content)
    return dictionaries


def any_to_uid(source):
    """Convert an item into a UID."""
    from Content import Content
    if type(source) is str:
        validate_uid(source)
        return source
    if type(source) is dict:
        validate_dict(source)
        validate_uid(source['uid'])
        return source['uid']
    if isinstance(source, Content):
        source.validate()
        return source.uid
    raise TypeError('This function expects a uid, dictionary, or a class.')


def any_to_dict(source):
    """Convert an item into a dictionary."""
    from Content import Content
    if type(source) is str:
        validate_uid(source)
        return retrieve_dictionary_by_uid(source)
    if type(source) is dict:
        validate_dict(source)
        return source
    if isinstance(source, Content):
        source.validate()
        return source.to_dict()
    raise TypeError('This function expects a uid, dictionary, or a class.')


def any_to_class(source):
    """Convert an item into a class."""
    from Content import Content
    if isinstance(source, Content):
        source.validate()
        return source
    source = any_to_dict(source)
    if source['type'] == 'clip':
        from Clip import Clip
        return Clip(source)
    if source['type'] == 'episode':
        from Episode import Episode
        return Episode(source)
    if source['type'] == 'project':
        from Project import Project
        return Project(source)
    raise TypeError('This function expects a uid, dictionary, or a class.')


def list_to_uids(source_list):
    """Convert all items in a list into UIDs."""
    validate_list(source_list)
    new_list_of_uids = []
    for index, source in enumerate(source_list):
        new_list_of_uids.append(any_to_uid(source))
    return new_list_of_uids


def list_to_dicts(source_list):
    """Convert all items in a list into dictionaries."""
    validate_list(source_list)
    new_list_of_dicts = []
    for index, source in enumerate(source_list):
        new_list_of_dicts.append(any_to_dict(source))
    return new_list_of_dicts


def list_to_classes(source_list):
    """Convert all items in a list into classes."""
    validate_list(source_list)
    new_list_of_classes = []
    for index, source in enumerate(source_list):
        new_list_of_classes.append(any_to_class(source))
    return new_list_of_classes


def access_classes(type_):
    """Return list of classes of a given type."""
    validate_content_type(type_)
    data = access_dictionary(type_)
    return list_to_classes(data)


def access_all_classes():
    """Return list of all classes."""
    data = access_all_dictionaries()
    return list_to_classes(data)


def save_classes(source_list):
    """Save all classes in a list."""
    validate_list(source_list)
    for index, content in enumerate(source_list):
        content.save()


def get_episode_num(string):
    """Determine the episode number from the title and return it as an integer."""
    for i, char in enumerate(string):
        if char == ":":
            return int(string[i - 3:i])


def convert_to_seconds(string):
    """Convert any input to an integer representation of seconds and return it."""
    string = str(string)
    if ":" in string:
        # Assume "HH:MM:SS" format
        try:
            string = [int(x) for x in string.split(":")]
        except ValueError:
            # Allow while loop to handle invalid input.
            return None
        while len(string) < 3:
            string.insert(0, 0)
        seconds = (string[0] * 3600) + (string[1] * 60) + (string[2])
    elif string.startswith("PT"):
        # Assume "contentDetails.duration" from YouTube Data API.
        original_string = string
        string = string[2:]
        seconds = 0
        num = ""
        for i, char in enumerate(string):
            if char.isdigit():
                num += char
            else:
                x = 1
                if char == "H":
                    x = 3600
                elif char == "M":
                    x = 60
                try:
                    seconds += int(num) * x
                except (ValueError, TypeError):
                    traceback.print_exc()
                    return original_string
                num = ""
    else:
        # Assume single integer.
        try:
            seconds = int(string)
        except ValueError:
            # Allow while loop to handle input.
            return None
    return seconds


def backup_files(callback):
    """Back up all JSON files before executing function."""
    def wrapped():
        backup_project_data = list(access_dictionary("project"))
        backup_clip_data = list(access_dictionary("clip"))
        backup_episode_data = list(access_dictionary("episode"))
        try:
            callback()
        except (ValueError, KeyError, AttributeError, TypeError, FileNotFoundError):
            update_file("project", backup_project_data)
            update_file("clip", backup_clip_data)
            update_file("episode", backup_episode_data)
            print("All files were reverted to a back-up state.")
            traceback.print_exc()
            sys.exit()
    return wrapped
