"""functions for handling files of data coming into the system."""


import tablib


def persist_source_file(source_file):
    """Saves an uploaded source file to a work directory."""
    pass


def create_dataset(source_file):
    """Returns a Tablib dataset from a given source file."""
    pass


def clean_headers(dataset):
    """Clean the headers of the existing dataset.

    To clean, we strip white space and common joining symbols.
    And, we convert everything to lowercase.
    """
    symbols = {
        ord('_'): None,
        ord('-'): None,
        ord('"'): None,
        ord(' '): None,
        ord("'"): None,
    }

    for header in dataset.headers:
        header.translate(symbols).lower()

    value = dataset
    return value


def get_header_maps():
    value = []
    #header_maps = HeaderMap.objects.all()
    #for map in header_maps:
    #   value.append((map.s, [m.s for m in map.alt_set.all()]))

    #actually I want a dict
    return value


def normalize_headers(dataset):
    """Normalize the headers of the existing dataset.

    Headers are normalized according to a defalt set of string
    mappings, and sets of related strings entered via site admins.
    """
    #header_maps = get_header_maps() - want DICT, not list
    for header in dataset.headers:
        try:
            new = header_maps[header]
        except KeyError:
            new = header
        value.append(new)
    return value


def validate_data_structure(dataset):
    """Validate the data structure against a template"""
    # get template
    # validate headers
    # validate nodes
    # return tuple of (bool, list(co-ordinates))
    # the list will match the bool value, so if it is false
    # a list of false co-ordinates, and if true, a list of true
    # presuming i can use the list of tru in subsequent function
    # need to see if that is so
    pass


def validate_data_values(dataset):
    """Validate that the data values match the expected input"""
    # check type matches expected
    # return tuple of (bool, list(co-ordinates))
    # the list will match the bool value, so if it is false
    # a list of false co-ordinates, and if true, a list of true
    # presuming i can use the list of tru in subsequent function
    # need to see if that is so
    pass


def dataset_to_db(dataset):
    """Save a dataset to the database"""
    pass
