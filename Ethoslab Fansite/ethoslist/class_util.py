import os
import json
from random import randint

"""Utility function for Ethoslist Classes"""


def validate_list(list_):
    if type(list_) is not list:
        raise TypeError('This function expects a list.')


def validate_type(string):
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


def generate_uid(len_=5):
    """Generate and return a UID."""
    characters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    uid = ''
    for i in range(len_):
        roll = randint(0, len(characters))
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
    validate_type(type_)
    relative_path = 'data/' + type_ + 's.json'
    absolute_path = os.path.dirname(__file__)
    return os.path.join(absolute_path, relative_path)


def access_dictionary(type_):
    """Access and return specific JSON file as an array of dictionaries."""
    validate_type(type_)
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


def get_object_type(data):
    """Determine object type of data and return it as a string."""
    from Content import Content
    if type(data) is list:
        data = data[0]
    if type(data) is dict and 'type' in data.keys():
        if data['type'] is not None:
            validate_type(data['type'])
            return data['type']
    elif isinstance(data, Content):
        if data.type is not None:
            validate_type(data.type)
            return data.type
    else:
        raise TypeError('Could not determine object type.')


def validate_list_uniformity(data, type_=None):
    """Ensure that all elements of a list are of the same data type and object type."""
    if type(data) is not list:
        raise TypeError('Data is not a list.')
    data_type = type(data[0])
    if type_ is not None:
        validate_type(type_)
        object_type = type_
    else:
        object_type = get_object_type(data)
    for index, value in enumerate(data):
        if not type(value) == data_type:
            raise TypeError('List contains different data types.')
        if not get_object_type(value) == object_type:
            raise TypeError('List contains different object types.')


def update_file(type_, data):
    """Save modified array of dictionaries to the corresponding JSON file."""
    validate_type(type_)
    validate_list_uniformity(data, type_)
    file_path = path_to(type_)
    with open(file_path, "w") as json_data:
        json.dump(data, json_data)


def retrieve_dictionary_by_uid(uid, type_=None):
    """Return dictionary with matching uid."""
    validate_uid(uid)
    if type_ is not None:
        validate_type(type_)
        data = access_dictionary(type_)
    else:
        data = access_all_dictionaries()
    for index, dictionary in enumerate(data):
        if dictionary['uid'] == uid:
            return dictionary
    raise FileNotFoundError('Dictionary of type \'{}\' with id \'{}\' was not found.'.format(type_, uid))


def retrieve_list_of_dictionaries_by_uid(list_, type_=None):
    """Return list of dictionaries corresponding to UIDs in list."""
    validate_uid_list(list_)
    dictionaries = []
    if type_ is None:
        data = access_all_dictionaries()
    else:
        validate_type(type_)
        data = access_dictionary(type_)
    for index, content in enumerate(data):
        if content['uid'] in list_:
            dictionaries.append(content)
    return dictionaries
