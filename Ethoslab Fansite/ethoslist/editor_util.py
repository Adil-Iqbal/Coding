from class_util import *
# from Clip import Clip
from Episode import Episode
# from Project import Project


def dict_to_class(dictionary):
    """Convert a dictionary into a class."""
    if type(dictionary) is dict and 'type' in dictionary.keys():
        raise TypeError('This function expects a dictionary with a valid type parameter')
    validate_type(dictionary['type'])
    if dictionary['type'] == 'clip':
        return Clip(dictionary)
    elif dictionary['type'] == 'episode':
        return Episode(dictionary)
    else:
        return Project(dictionary)


def list_of_dicts_to_classes(list_):
    """Convert a list of dictionaries into a list of classes."""
    validate_list_uniformity(list_)
    error_message = 'This function expects a list of dictionaries'
    if type(list_) is not list:
        raise TypeError(error_message)
    classes = []
    for index, dictionary in enumerate(list_):
        if type(dictionary) is not dict:
            raise TypeError(error_message)
        classes.append(dict_to_class(dictionary))
    return classes


def list_of_uids_to_classes(list_):
    validate_uid_list(list_)
    dictionaries = retrieve_list_of_dictionaries_by_uid(list_)
    return list_of_dicts_to_classes(dictionaries)




def access_classes(type_):
    """Return list of classes of a given type."""
    validate_type(type_)
    data = access_dictionary(type_)
    return list_of_dicts_to_classes(data)


def access_all_classes():
    """Return list of all classes."""
    data = access_all_dictionaries()
    return list_of_dicts_to_classes(data)


def save_list_of_classes(list_):
    """Save all classes in a list."""
    validate_list(list_)
    for index, class_ in enumerate(list_):
        class_.save()
