import os
import sys
import json
import requests
import traceback
import webbrowser
from time import sleep
from math import log10, floor
import dateutil.parser as to_datetime

"""Utility functions for primary JSON Editor application."""

url = "https://www.googleapis.com/youtube/v3/videos"
api_key = "AIzaSyBoVWZevLKCgLn_v-KNyT7gt3fsr_JdA4M"
list_of_types = ["clip", "episode", "project"]

default_begin_date = "9000-12-31T17:00:00.000Z"
default_last_updated_date = "1800-01-01T17:00:00.000Z"

clip_description_max_length = 120
project_description_max_length = 500


def round_sig(x, sig=4):
    """Round to designated number of significant figures."""
    try:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)
    except ValueError:
        return 0.0


def get_episode_num(string):
    """Returns the episode number as an integer."""
    for i, char in enumerate(string):
        if char == ":":
            return int(string[i - 3:i])


def type_check(string):
    """Check to see if param is a valid object type."""
    if string not in list_of_types:
        raise TypeError("Parameter must equal \'clip\', \'project\', or \'episode.\'")


def access_file(obj_type):
    """Return the data from designated JSON file."""
    type_check(obj_type)
    filename = obj_type + "s.json"
    with open(filename, "r") as j_data:
        d_data = json.load(j_data)
        return d_data


def update_file(data, obj_type=None):
    """Store updated data into JSON file."""
    try:
        obj_type = data[0]["type"]
    except IndexError:
        if obj_type is None:
            raise Exception(
                "Could not identify object type. Data variable is empty and \'obj_type\' param was undeclared.")
    filename = obj_type + "s.json"
    with open(filename, "w") as j_data:
        json.dump(data, j_data)


def backup_files(callback):
    """Back up all JSON files before executing function."""
    def wrapped():
        backup_project_data = list(access_file("project"))
        backup_clip_data = list(access_file("clip"))
        backup_episode_data = list(access_file("episode"))
        try:
            callback()
        except:
            update_file(backup_project_data)
            update_file(backup_clip_data)
            update_file(backup_episode_data)
            print("All files were reverted to a back-up state.")
            traceback.print_exc()
            sys.exit()
        del backup_project_data
        del backup_episode_data
        del backup_clip_data
    return wrapped


def load_obj_by_id(id_, obj_type):
    """Return an object by it's ID and type."""
    type_check(obj_type)
    data = access_file(obj_type)
    return data[id_]


def save_to_file(obj):
    """Save an object in it's corresponding JSON file."""
    data = access_file(obj["type"])
    if obj["id"] is None:
        obj["id"] = len(data)
        data.append(obj)
    else:
        data[obj["id"]] = obj
    update_file(data)


def replace_in_list(list_, old_item, new_item):
    """Replace an old item in a list and return the list."""
    try:
        index_ = list_.index(old_item)
    except ValueError:
        return list_
    list_[index_] = new_item
    return list_


def force_id_index_alignment():
    """Re-assign all objects' IDs to their indexed position in the list."""
    for obj_type in list_of_types:
        data = access_file(obj_type)
        for index, item in enumerate(data):
            if index != item["id"]:
                if item["type"] == "clip":
                    ep_id = item["from_episode"]["id"]
                    episode = load_obj_by_id(ep_id, "episode")
                    episode["associated_clips"] = replace_in_list(episode["associated_clips"], item["id"], index)
                    save_to_file(episode)
                    for pr_id in item["associated_projects"]:
                        project = load_obj_by_id(pr_id, "project")
                        project["clip_ids"] = replace_in_list(project["clip_ids"], item["id"], index)
                        save_to_file(project)
                if item["type"] == "episode":
                    for clip_id in item["associated_clips"]:
                        clip = load_obj_by_id(clip_id, "clip")
                        clip["from_episode"]["id"] = index
                        save_to_file(clip)
                if item["type"] == "project":
                    for pr_id in item["related_projects"]:
                        project = load_obj_by_id(pr_id, "project")
                        project["related_projects"] = replace_in_list(project["related_projects"], item["id"], index)
                        save_to_file(project)
                    for clip_id in item["clip_ids"]:
                        clip = load_obj_by_id(clip_id, "clip")
                        clip["associated_projects"] = replace_in_list(clip["associated_projects"], item["id"], index)
                        save_to_file(clip)
                item["id"] = index
        update_file(data)


def scan_files_for_alignment():
    """Scan files to ensure their ID's match their indexed position."""
    for obj_type in list_of_types:
        data = access_file(obj_type)
        for index, entry in enumerate(data):
            if not (entry["id"] == index):
                raise IndexError("Indexes in the JSON file do not align. Please fix!")
    print("All id's align with their indexes.")


def convert_to_seconds(string):
    """Returns number of seconds as an integer."""
    string = str(string)
    if ":" in string:
        # Assume "HH:MM:SS" format
        try:
            string = [int(x) for x in string.split(":")]
        except ValueError:
            return None  # Allow while loop to handle invalid input.
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


def blank(obj_type):
    """Creates and returns a blank project, episode, or clip template."""
    if obj_type == "project":
        return {
            "id": None,
            "type": "project",
            "title": None,
            "description": None,
            "media": None,
            "status": -1,
            "clip_ids": [],
            "begin_date": default_begin_date,
            "last_updated": default_last_updated_date,
            "location": {
                "season": None,
                "dimension": "",
                "x": None,
                "y": None,
                "z": None
            },
            "related_projects": []
        }
    elif obj_type == "clip":
        return {
            "id": None,
            "type": "clip",
            "title": None,
            "description": None,
            "from_episode": {
                "youtube_id": None,
                "id": None,
                "published_at": None
            },
            "start": 0,
            "end": 0,
            "associated_projects": []
        }
    elif obj_type == "episode":
        return {
            "id": None,
            "type": "episode",
            "youtube_id": None,
            "title": None,
            "episode": None,
            "description": None,
            "published_at": None,
            "duration": None,
            "media": None,
            "associated_clips": [],
            "curation": {
                "curated_time": 0,
                "percentage": 0.0
            }
        }
    else:
        raise TypeError("Argument must equal 'clip' or 'project' or 'episode'.")


def key_check(type_, attr):
    """Check to see if an attribute belongs to the object type."""
    type_check(type_)
    dict_ = blank(type_)
    if attr not in dict_.keys():
        raise AttributeError(type_.title() + " does not contain the \'" + attr + "\' attribute.")
    del dict_


def is_unique(title, type_):
    """Check if a selected title is unique."""
    data = access_file(type_)
    if len(data) == 0:
        return True
    for obj in data:
        if obj["title"] == title:
            return False
    return True


def request_episode(youtube_id):
    """Retrieve episode and convert into episode object for saving."""
    parameters = {
        "part": "snippet,contentDetails",
        "id": youtube_id,
        "key": api_key,
    }
    result = requests.request(method="get", url=url, params=parameters)
    j_result = json.loads(result.text)
    new_episode = blank("episode")
    new_episode["youtube_id"] = j_result['items'][0]['id']
    new_episode["title"] = j_result['items'][0]['snippet']['title']
    new_episode["episode"] = get_episode_num(j_result['items'][0]['snippet']['title'])
    new_episode["description"] = j_result['items'][0]['snippet']['description']
    new_episode["published_at"] = j_result['items'][0]['snippet']['publishedAt']
    new_episode["duration"] = convert_to_seconds(j_result['items'][0]['contentDetails']['duration'])
    new_episode["media"] = j_result['items'][0]['snippet']['thumbnails']
    save_to_file(new_episode)


def is_valid_youtube_id(potential_id):
    """Check if param can be used as a YouTube ID."""
    if type(potential_id) is not str:
        return False
    if len(potential_id) is not 11:
        return False
    for char in potential_id:
        if not char.isalnum() and char is not "-" and char is not "_":
            return False
    return True


def sort_clip_ids(clip_ids):
    """Sort a list of clip ID's chronologically."""
    if len(clip_ids) <= 1:
        return clip_ids
    # Pair clip ids to their episode's publish dates.
    id_list = []
    data = access_file("clip")
    for id_ in clip_ids:
        new_dict = {
            "id": id_,
            "date": data[id_]["from_episode"]["published_at"]
        }
        id_list.append(new_dict)
    # Convert date string to datetime object.
    for item in id_list:
        item["date"] = to_datetime.parse(item["date"])
    # Bubble sort algorithm
    for i in range(1, len(id_list)):
        for j in range(len(id_list) - i):
            if id_list[j]["date"] > id_list[j + 1]["date"]:
                id_list[j], id_list[j + 1] = id_list[j + 1], id_list[j]
    # Strip output of datetime objects.
    new_list = []
    for item in id_list:
        new_list.append(item["id"])
    return new_list


def refresh_project_dates(proj):
    """Update a project's datetime information with reference to clip data."""
    if len(proj["clip_ids"]) == 0:
        return default_begin_date, default_last_updated_date
    # Sort clips from earliest to latest.
    proj["clip_ids"] = sort_clip_ids(proj["clip_ids"])
    first_clip = load_obj_by_id(proj["clip_ids"][0], "clip")
    last_clip = load_obj_by_id(proj["clip_ids"][-1], "clip")
    # Update begin date.
    proj_begin_date = to_datetime.parse(proj["begin_date"])
    first_episode_date = first_clip["from_episode"]["published_at"]
    first_episode_date = to_datetime.parse(first_episode_date)
    if first_episode_date < proj_begin_date:
        proj_begin_date = first_episode_date
    # Update last updated date.
    proj_last_updated = to_datetime.parse(proj["last_updated"])
    last_episode_date = last_clip["from_episode"]["published_at"]
    last_episode_date = to_datetime.parse(last_episode_date)
    if last_episode_date > proj_last_updated:
        proj_last_updated = last_episode_date
    # Return values in ISO format.
    return proj_begin_date.isoformat(), proj_last_updated.isoformat()


def refresh_curation_data(obj):
    """Calculate an episode object's curation data based on it's associated clips."""
    total_runtime = [False for x in range(obj["duration"])]
    for clip_id in obj["associated_clips"]:
        clip = load_obj_by_id(clip_id, "clip")
        for i in range(clip["start"], clip["end"]):
            total_runtime[i] = True
    obj["curation"]["curated_time"] = total_runtime.count(True)
    obj["curation"]["percentage"] = round_sig(((obj["curation"]["curated_time"] / obj["duration"]) * 100), sig=4)
    return obj["curation"]


def error_catch(a, b, action=None):
    """Detect a faulty link."""
    if a["type"] == "clip" and b["type"] == "project":
        a_list = a["associated_projects"]
        b_list = b["clip_ids"]
    if a["type"] == "clip" and b["type"] == "episode":
        a_list = a["associated_projects"]
        b_list = b["associated_clips"]
    if a["type"] == "project" and b["type"] == "project":
        a_list = a["related_projects"]
        b_list = b["related_projects"]
    if action == "break":
        if (a["id"] not in b_list) and (b["id"] not in a_list):
            raise Exception("Objects do not have a link to break.")
    else:
        if (a["id"] in b_list) and (b["id"] in a_list):
            raise Exception("Objects are already linked.")
    if (a["id"] in b_list) and (b["id"] not in a_list):
        raise Exception(
            "Faulty link detected: " + a["type"] + "[" + str(a["id"]) + "] is missing a reference to " + b[
                "type"] + "[" + str(
                b["id"]) + "].")
    if (a["id"] in b_list) and (b["id"] not in a_list):
        raise Exception(
            "Faulty link detected: " + b["type"] + "[" + str(b["id"]) + "] is missing a reference to " + a[
                "type"] + "[" + str(
                a["id"]) + "].")


def link_clip_to_project(clip, proj, action=None):
    """Make or break the link between a project and a clip."""
    error_catch(clip, proj, action=action)
    if action == "break":
        clip["associated_projects"].remove(proj["id"])
        proj["clip_ids"].remove(clip["id"])
        proj["begin_date"], proj["last_updated"] = refresh_project_dates(proj)
        if len(proj["clip_ids"]) == 0:
            proj["status"] = -1
    else:
        clip["associated_projects"].append(proj["id"])
        proj["clip_ids"].append(clip["id"])
        proj["begin_date"], proj["last_updated"] = refresh_project_dates(proj)
        if proj["status"] < 0:
            proj["status"] = 0
    return clip, proj


def link_clip_to_episode(clip, epi, action=None):
    """Make or break the link between an episode and a clip."""
    error_catch(clip, epi, action=action)
    if action == "break":
        epi["associated_clips"].remove(clip["id"])
        clip["from_episode"]["id"] = None
        clip["from_episode"]["youtube_id"] = None
        clip["from_episode"]["published_at"] = None
        epi["curation"] = refresh_curation_data(epi)
    else:
        epi["associated_clips"].append(clip["id"])
        clip["from_episode"]["id"] = epi["id"]
        clip["from_episode"]["youtube_id"] = epi["youtube_id"]
        clip["from_episode"]["published_at"] = epi["published_at"]
        epi["curation"] = refresh_curation_data(epi)
    return clip, epi


def link_project_to_project(x, y, action=None):
    """Make or break the link between two projects."""
    error_catch(x, y, action=action)
    if action == "break":
        x["related_projects"].remove(y["id"])
        y["related_projects"].remove(x["id"])
    else:
        x["related_projects"].append(y["id"])
        y["related_projects"].append(x["id"])
    return x, y


def link(a, b, action=None):
    """Make or break any link."""
    if (a["type"] == "clip") and (b["type"] == "project"):
        a, b = link_clip_to_project(a, b, action=action)
    elif (a["type"] == "project") and (b["type"] == "clip"):
        b, a = link_clip_to_project(b, a, action=action)
    elif (a["type"] == "clip") and (b["type"] == "episode"):
        a, b = link_clip_to_episode(a, b, action=action)
    elif (a["type"] == "episode") and (b["type"] == "clip"):
        b, a = link_clip_to_episode(b, a, action=action)
    elif (a["type"] == "project") and (b["type"] == "project"):
        a, b = link_project_to_project(a, b, action=action)
    else:
        raise TypeError("You can only link clip to project, clip to episode, or project to project.")
    save_to_file(a)
    save_to_file(b)


@backup_files
def delete_project(project, firm=True):
    """Delete a project object."""
    if project["status"] == -2:
        for id in project["related_projects"]:
            linked_proj = load_obj_by_id(id, "project")
            linked_proj, project = link_project_to_project(linked_proj, project, action="break")
            save_to_file(linked_proj)
        for id in project["clip_ids"]:
            linked_clip = load_obj_by_id(id, "clip")
            if len(linked_clip["associated_projects"]) <= 1:
                str_id = "[" + str(linked_clip["id"]) + "]"
                print("Clip " + str_id + " is now obsolete...")
            linked_clip, project = link_clip_to_project(linked_clip, project, action="break")
            save_to_file(linked_clip)
        data = access_file("project")
        del data[project["id"]]
        update_file(data, "project")
        force_id_index_alignment()
    elif firm:
        raise Exception(
            "Project [index: " + str(project["id"]) + "] must be marked for deletion before any action is taken.")
    

def build_url(clip_object, autoplay=False):
    """Build and return URL based on clip object."""
    if clip_object["type"] != "clip":
        raise Exception("Wrong object type. This function only accepts clip objects.")
    id_ = clip_object["from_episode"]["youtube_id"]
    start = "&start=" + str(clip_object["start"])
    end = "&end=" + str(clip_object["end"])
    other_params = "&fs=1&iv_load_policy=3&showinfo=1&rel=0&cc_load_policy=0"
    autoplay = "?autoplay=1" if autoplay else "?autoplay=0"
    return "https://www.youtube.com/embed/" + id_ + autoplay + other_params + start +  end


def build_embed(clip_object, autoplay=False):
    """Build and return the iframe that will hold clips."""
    url = build_url(clip_object, autoplay=autoplay)
    return "<iframe frameborder=\"0\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\"width=\"788.54\" height=\"443\" type=\"text/html\" src=" + url + "></iframe>"


def view_clip(clip_object):
    """Build and open an html file with clip embedded."""
    title = "<head><title>" + clip_object["title"] + "</title></head>"
    h1 = "<h1>" + clip_object["title"] + "</h1>"
    h2 = "<h2>" + clip_object["description"] + "</h2>"
    embed = build_embed(clip_object, autoplay=True)
    html = "<html>" + title + "<body style=\"font-family: verdana\">" + embed + h1 + h2 + "</body></html>"
    with open("render_clip.html", "w+") as page:
        page.write(html)
    webbrowser.open('file://' + os.path.realpath("render_clip.html"))
    sleep(5)
    os.remove("render_clip.html")
    