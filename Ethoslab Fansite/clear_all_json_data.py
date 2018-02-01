import json

## The follow code was taken from ethoslist.util
list_of_types = ["clip", "episode", "project"]

def type_check(string):
    if string not in list_of_types:
        raise TypeError("Parameter must equal \'clip\', \'project\', or \'episode.\'")


def access_file(obj_type):
    """Return the data from designated JSON file."""
    type_check(obj_type)
    filename = obj_type + "s.json"
    with open(filename, "r") as j_data:
        d_data = json.load(j_data)
        return d_data


def update_file(data, obj_type):
    """Store updated data into JSON file."""
    type_check(obj_type)
    filename = obj_type + "s.json"
    with open(filename, "w") as j_data:
        json.dump(data, j_data)


## Clear all script.
print("If you are absolutely sure you want to do this...")
input_ = input("Type \'CLEAR THE WAY\' here: ")
if input_=="CLEAR THE WAY":
    data = access_file("episode")
    for episode in data:
        episode["curation"]["curated_time"] = 0
        episode["curation"]["percentage"] = 0.0
        episode["associated_clips"] = []
    update_file(data, "episode")
    update_file([], "clip")
    update_file([], "project")
    print("GOD HAVE MERCY ON YOUR SOUL!")
else:
    print("Never come back.")