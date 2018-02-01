import os
import sys
from pprint import pprint
from .ethoslist_util import *


def global_command(string):
    if string == "-exit":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Thank you for using the Etho\'s List JSON Editor.")
        sys.exit()
    if string == "-restart":
        scan_files_for_alignment()
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    if string == "-clear":
        os.system('cls' if os.name == 'nt' else 'clear')


def show_display(display=None, spacing=False):
    if display is not None and type(display) is not list:
        display = [display]
    if display is not None:
        for index, line in enumerate(display):
            line = str(line)
            if index == 0:
                line = ("\n" + line) if spacing else line
            elif index == len(display) - 1:
                line = (line + "\n") if spacing else line
            print(line)


def respond_bool(question, display=None, spacing=False):
    """Return boolean response."""
    while True:
        show_display(display, spacing)
        answer = input(str(question) + " (Y/N): ")
        global_command(answer)
        if answer.lower() == "n":
            return False
        elif answer.lower() == "y":
            return True
        print("Please enter \"Y\" to confirm or \"N\" to cancel.")


def respond_int(question, display=None, min_=None, max_=None, spacing=False):
    """Return integer response."""
    limit = None
    if type(min_) is not None:
        try:
            min_= int(min_)
        except (ValueError, TypeError):
            min_ = None
    if type(max_) is not None:
        try:
            max_= int(max_)
        except (ValueError, TypeError):
            max_ = None
    if min_ is not None and max_ is not None:
        if max_ <= min_:
            max_ = None
            min_ = None
    if type(min_) is int and max_ is None:
        limit = "Please enter a number greater than or equal to " + str(min_) + "."
    elif min_ is None and type(max_) is int:
        limit = "Please enter a number less than " + str(max_) + "."
    elif type(min_) is int and type(max_) is int:
        limit = "Please enter a number between " + str(min_) +" and "+ str(max_) +"."
    answer = None
    while type(answer) is not int:
        show_display(display, spacing)
        answer = input(str(question))
        global_command(answer)
        try:
            answer = int(answer)
            if min_ is not None:
                if answer < min_:
                    answer = None
                    print(limit)
            if max_ is not None and answer is not None:
                if answer >= max_:
                    answer = None
                    print(limit)
        except (ValueError, TypeError):
            answer = None
    return answer


def respond_str(question, display=None, min_=None, max_=None, spacing=False, confirm=False):
    question = (str(question) + " ") if question[-1] is not " " else str(question)
    limit = None
    if type(min_) is not None:
        try:
            min_ = int(min_)
        except (ValueError, TypeError):
            min_ = None
    if type(max_) is not None:
        try:
            max_ = int(max_)
        except (ValueError, TypeError):
            max_ = None
    if min_ is not None and max_ is not None:
        if max_ < min_:
            max_ = None
            min_ = None
    if type(min_) is int and max_ is None:
        limit = "The length of your answer must be greater than " + str(min_) + "."
    elif min_ is None and type(max_) is int:
        limit = "The length of your answer must be less than " + str(max_) + "."
    elif type(min_) is int and type(max_) is int:
        if min_ == max_:
            limit = "The length of your answer must be exactly " + str(min_) + "."
        else:
            limit = "The length of your answer must be between " + str(min_) + " and " + str(max_) + "."
    answer = None
    while type(answer) is not str:
        show_display(display, spacing)
        answer = input(str(question))
        global_command(answer)
        if min_ is not None:
            if len(answer) < min_:
                answer = None
                print(limit)
        if max_ is not None and answer is not None:
            if len(answer) > max_:
                answer = None
                print(limit)
        if confirm and answer is not None:
            display = "You entered: " + answer
            cf_question = "Are you sure?"
            if not respond_bool(cf_question, display):
                answer = None
    return answer


def set_title(type_, title=None):
    """Set's a title for a clip or a project."""
    type_check(type_)
    if title is None:
        while True:
            question = "Enter the title of your new " + type_ + ": "
            title = respond_str(question, confirm=True)
            if is_unique(title, type_):
                print("Title as been set to '" + title + ".'")
                return title
            else:
                print("That title is already taken. Please enter a new title.")
    else:
        while True:
            question = "Enter the new title of your " + type_ + ": "
            new_title = respond_str(question, confirm=True)
            if is_unique(new_title, type_):
                line1 = "Previous Title: " + title
                line2 = "New Title: " + new_title
                display = [line1, line2]
                question = "Are you sure you want to change the title?"
                if respond_bool(question=question, display=display, spacing=True):
                    print("The title of the " + type_ + " was changed to: " + new_title)
                    return new_title
                else:
                    print("The title was not changed.")
                    return title
            print("That title is already taken. Please enter a new title.")


def set_description(type_, description=None):
    """Set's a description for a clip or a project."""
    type_check(type_)
    x = clip_description_max_length
    if type_ == "project":
        x = project_description_max_length
    if description is None:
        description = respond_str("Enter the description of your new " + type_ + ": ", max_=x)
    else:
        new_description = respond_str("Enter the new description for your " + type_ + ": ", max_=x)
        line1 = "Previous Description: " + description + "\n"
        line2 = "New Description: " + new_description
        display = [line1, line2]
        question = "Are you sure you want to change the description?"
        if respond_bool(question, display, spacing=True):
            print("The description of the " + type_ + " was changed to: " + new_description)
            return new_description
        else:
            print("The description was not changed.")
    return description


def set_dimension():
    """Set the dimension for a location object."""
    line1 = "In which dimension was this project built?"
    line2 = "1. The Overworld."
    line3 = "2. The Nether."
    line4 = "3. The End."
    display = [line1, line2, line3, line4]
    question = "Enter the corresponding number of your answer: "
    dim = respond_int(question, display, min_=1, max_=4)
    if dim == 1:
        return "overworld", "the Overworld."
    elif dim == 2:
        return "nether", "the Nether."
    elif dim == 3:
        return "the_end", "the End."


def set_coord(msg):
    """Set the coordinates of a location object."""
    while True:
        response = input(msg)
        global_command(response)
        try:
            return float(response)
        except (ValueError, TypeError):
            print("You must enter an integer or floating point number.")


def set_location(loc):
    """Set the location of a project object."""
    line1 = "Do you know the location of this project?"
    line2 = "1. Not at all."
    line3 = "2. The dimension only."
    line4 = "3. The dimension and the coordinates."
    display = [line1, line2, line3, line4]
    question = "Enter the corresponding number of your answer: "
    gran = respond_int(question, display, min_=1, max_=4)
    loc["season"] = 2
    if gran == 1:
        loc["dimension"] = "overworld"
        print("Project location has been set to default.")
        return loc
    elif gran == 2:
        loc["dimension"], msg = set_dimension()
        print("The project's dimension has been set to: " + msg)
        return loc
    elif gran == 3:
        loc["dimension"], msg = set_dimension()
        print("The project's dimension has been set to: " + msg)
        loc["x"] = set_coord("Set X-coordinate: ")
        loc["y"] = set_coord("Set Y-coordinate: ")
        loc["z"] = set_coord("Set Z-coordinate: ")
        coords = str(loc["x"]) + ", " + str(loc["y"]) + ", " + str(loc["z"])
        print("The project's coordinates have been set to: " + coords)
        return loc
    else:
        print("Please enter the number of the corresponding option below...")


def display_object(obj_type, id_=-1):
    type_check(obj_type)
    question = "Would you like to see the " + obj_type + "?"
    confirm = respond_bool(question)
    if confirm:
        data = access_file(obj_type)
        pprint(data[id_])
        confirm = respond_bool("Are you ready to move on?")
        return


def create_new_project():
    """Builds a stores a new project object."""
    new_proj = blank("project")
    new_proj["title"] = set_title(new_proj["type"])
    new_proj["description"] = set_description(new_proj["type"])
    new_proj["location"] = set_location(new_proj["location"])
    print("New project has been created!")
    display_object("project")
    save_to_file(new_proj)


def create_new_episode():
    """Interface for creating an episode object."""
    question = "Please enter the new episode's YouTube ID: "
    id_ = respond_str(question, min_=11, max_=11)
    if is_valid_youtube_id(id_):
        try:
            request_episode(id_)
            print("New episode has been created!")
            display_object("episode")
        except IndexError:
            print("There was a problem requesting the video...")
            question = "Would you like to see the error?"
            show_err = respond_bool(question)
            if show_err:
                traceback.print_exc()


def find_and_return_object(obj_type):
    obj_type = str(obj_type)
    type_check(obj_type)
    data = access_file(obj_type)
    if len(data) > 0:
        while True:
            question = "Please enter the ID of the " + obj_type + ": "
            id_ = respond_int(question, min_=0, max_=len(data))
            line1 = obj_type.title() + " found!"
            line2 = data[id_]["title"]
            line3 = data[id_]["description"][:len(line2)] + "\n"
            display = [line1, line2, line3]
            question = "Is this the correct " + obj_type.lower() + "?"
            confirm = respond_bool(question, display)
            if confirm:
                return data[id_]
    else:
        print("There are no saved " + obj_type + "s.")
        print("Please create a new "+ obj_type +" and try again.")
        main()


def set_start(max_end, end=None):
    if end is None:
        end = max_end
    start = None
    while type(start) is not int:
        question = "Please enter the START time: "
        start = respond_str(question)
        if start == "":
            start = 0
        start = convert_to_seconds(start)
        if start < 0:
            start = 0
        if start > end:
            start = end - 1
    return start


def set_end(max_end, start):
    end = None
    while type(end) is not int:
        question = "Please enter the END time: "
        end = respond_str(question)
        if end == "":
            end = max_end
        end = convert_to_seconds(end)
        if end > max_end:
            end = max_end
        if end < start:
            print("The END TIME must be greater than the START TIME("+str(start)+" seconds).")
            end = None
    return end


def set_duration(max_end):
    start = set_start(max_end)
    end = set_end(max_end, start)
    return start, end


def change_duration(object_, start=False, end=False):
    if (start and end) or (not start and not end):
        raise Exception("Improper usage. Params must be used in XOR fashion.")
    max_end = load_obj_by_id(object_["from_episode"]["id"], "episode")
    max_end = max_end["duration"]
    if start:
        new_start = set_start(max_end, object_["end"])
        line1 = "Current start time: " + str(object_["start"])
        line2 = "New start time: " + str(new_start)
        display = [line1, line2]
        choice = respond_bool("Are you sure?", display)
        if choice:
            print("Start time has been changed to: " + str(new_start))
            return new_start
        else:
            print("Start time was not changed.")
            return object_["start"]
    if end:
        new_end = set_end(max_end, object_["start"])
        line1 = "Current end time: " + str(object_["end"])
        line2 = "New end time: " + str(new_end)
        display = [line1, line2]
        choice = respond_bool("Are you sure?", display)
        if choice:
            print("End time has been changed to: " + str(new_end))
            return new_end
        else:
            print("End time was not changed.")
            return object_["start"]


def change_episode(clip):
    id_ = clip["from_episode"]["id"]
    new_episode = find_and_return_object("episode")
    if new_episode["id"] == id_:
        print("No changes were made. Chosen parent was the same as current parent.")
        return clip
    old_episode = load_obj_by_id(id_, "episode")
    line1 = "Current parent: " + old_episode["title"]
    line2 = "New parent: " + new_episode["title"]
    display = [line1, line2]
    question = "Are you sure you want to change the parent episode?"
    confirm = respond_bool(question, display)
    if confirm:
        clip, old_episode = link_clip_to_episode(clip, old_episode, action="break")
        clip, new_episode = link_clip_to_episode(clip, new_episode)
        save_to_file(old_episode)
        save_to_file(new_episode)
        print("Changes were made successfully!")
        return clip
    else:
        print("No changes were made.")
        return clip


def change_project(clip, action=None):
    if action == "break":
        proj_list = clip["associated_projects"]
        if len(proj_list) == 1:
            selected_proj = load_obj_by_id(proj_list[0], "project")
        else:
            line1 = "Which project would you like to remove this clip from?"
            display = [line1]
            for index, proj_id in enumerate(clip["associated_projects"]):
                proj_obj = load_obj_by_id(proj_id, "project")
                display.append(str(index + 1) + ". " + proj_obj["title"].title())
            display.append(str(len(clip["associated_projects"]+1)) + ". Restart")
            #TODO: Finish this variable length menu display. Good luck to you.
        """---Do not edit below this line.---"""
        line1 = "Selected Clip: " + clip["title"]
        line2 = "Selected Project: " + selected_proj["title"]
        display = [line1, line2]
        question = "Are you sure you want to remove the clip from this project?"
        confirm = respond_bool(question, display)
        if confirm:
            clip, selected_proj = link_clip_to_project(clip, selected_proj, action="break")
            save_to_file(selected_proj)
            print("Changes were made successfully!")
            return clip
        else:
            print("No changes were made.")
            return clip
    else:
        new_project = find_and_return_object("project")
        if new_project["id"] in clip["associated_projects"]:
            print("No changes were made. Project is already associated with clip.")
            return clip
        line1 = "Selected Clip: " + clip["title"]
        line2 = "Selected Project: " + new_project["title"]
        display = [line1, line2]
        question = "Are you sure you want to add the clip to this project?"
        confirm = respond_bool(question, display)
        if confirm:
            clip, new_project = link_clip_to_project(clip, new_project)
            save_to_file(new_project)
            print("Changes were made successfully!")
            return clip
        else:
            print("No changes were made.")
            return clip


def create_new_clip():
    new_clip = blank("clip")
    # Declare saved objects to be acted upon.
    episode = find_and_return_object("episode")
    project = find_and_return_object("project")
    # Declare particulars of the clip and SAVE.
    new_clip["title"] = set_title(new_clip["type"])
    new_clip["description"] = set_description(new_clip["type"])
    max_end_time = episode["duration"]
    new_clip["start"], new_clip["end"] = set_duration(max_end_time)
    save_to_file(new_clip)
    # Link all objects together.
    link(new_clip, episode)
    link(new_clip, project)
    print("New clip has been created!")
    display_object("clip")


def menu_title(title=None, len_=40, min_len=40):
    if len_ < min_len:
        len_ = min_len
    if title == None:
        return "-" * len_
    title = str(title).upper()
    if len(title) > (len_ - 2):
        raise ValueError("Length of \'title\' parameter must no more than 38 characters.")
    title = (" " + title) if not title.startswith(" ") else title
    title = (title + " ") if not title.endswith(" ") else title
    from math import floor
    dash_len = floor((len_ - len(title)) / 2)
    title = (dash_len * "-") + title
    while len(title) < len_:
        title += "-"
    return title


def make_menu(title, options, min_len=40):
    options_ = list(options)
    for index, string in enumerate(options_):
        string = str(index + 1) + ". " + str(string).title()
        options_[index] = string
    max_ = len(max(options_))
    title_line = menu_title(str(title), max_, min_len)
    closing = menu_title(len_=max_, min_len=min_len)
    display = [title_line] + options_ + [closing]
    question = "Enter a number corresponding to the options above: "
    os.system('cls' if os.name == 'nt' else 'clear')
    return respond_int(question, display, min_=1, max_=(len(options_)+1), spacing=True)


def change_location(loc):
    previous_loc = dict(loc)
    line1 = "Season: " + str(previous_loc["season"])
    line2 = "Dimension: " + str(previous_loc["dimension"])
    line3 = "X: " + str(previous_loc["x"])
    line4 = "Y: " + str(previous_loc["y"])
    line5 = "Z: " + str(previous_loc["z"])
    display = [line1, line2, line3, line4, line5]
    question = "Would you like to change this location?"
    choice = respond_bool(question, display)
    if choice:
        new_loc = blank("project")
        new_loc = new_loc["location"]
        return set_location(new_loc)


def set_status(status):
    if type(status) is not int:
        raise TypeError("Project status must be an integer.")
    if -3 > status > 3:
        raise ValueError("Project status must be between -3 and 3.")
    status_key = {
     "-2": "marked for deletion",
     "-1": "newly created",
     "0": "work in progress",
     "1": "completed",
     "2": "abandoned"
    }
    line1 = "Current status: " + status_key[str(status)].title()
    if status < 0:
        print(line1)
        print("Status change request is denied.")
        if status == -1:
            print("Please add a clip to this project and try again.")
        return status
    line2 = "Would you like to change the status of this project?"
    line3 = "1. Change status to: " + status_key[str(0)].title()
    line4 = "2. Change status to: " + status_key[str(1)].title()
    line5 = "3. Change status to: " + status_key[str(2)].title()
    line6 = "4. Cancel."
    display = [line1, line2, line3, line4, line5, line6]
    question = "Enter a number corresponding to the options above: "
    choice = respond_int(question, display, min_=1, max_=6)
    if status == (choice-1):
        choice = 4  # If the selected status is the same as the current status, Cancel
    if choice == 4:
        print("Status was not changed.")
        return status
    else:
        line1 = "Current status: " + status_key[str(status)].title()
        line2 = "New status: " + status_key[str(choice-1)].title()
        display = [line1, line2]
        question = "Are you sure you would like to change the status?"
        confirm = respond_bool(question, display)
        if confirm:
            print("The status has been changed to: "+ status_key[str(choice-1)].title())
            return (choice-1)
        else:
            print("Status was not changed.")
            return status


def change_attr(attr, type_, action=None):
    type_check(type_)
    key_check(type_, attr)
    object = find_and_return_object(type_)
    if attr=="title":
        object[attr] = set_title(object["type"], object[attr])
    if attr=="description":
        object[attr] = set_description(object["type"], object[attr])
    if attr=="location":
        object[attr] = change_location(object[attr])
    if attr=="status":
        object[attr] = set_status(object[attr])
    if attr=="start":
        object[attr] = change_duration(object, start=True)
    if attr=="end":
        object[attr] = change_duration(object, end=True)
    if attr=="from_episode":
        object = change_episode(object)
    if attr=="associated_projects":
        object = change_project(object, action=action)
    save_to_file(object)
    display_object(type_, object["id"])


def modify_clip(title):
    option1 = "change title"
    option2 = "change description"
    option3 = "change start time"
    option4 = "change end time"
    option5 = "change parent episode"
    option6 = "link to project"
    option7 = "remove link to project"
    option8 = "restart"
    options = [option1, option2, option3, option4, option5, option6, option7, option8]
    choice = make_menu(title, options)
    print("\n" + menu_title(options[choice - 1]))
    if choice == 1:
        change_attr("title", "clip")
    elif choice == 2:
        change_attr("description", "clip")
    elif choice == 3:
        change_attr("start", "clip")
    elif choice == 4:
        change_attr("end", "clip")
    elif choice == 5:
        change_attr("from_episode", "clip")
    elif choice == 6:
        change_attr("associated_projects", "clip")
    elif choice == 7:
        change_attr("associated_projects", "clip", action="break")
    elif choice == 8:
        global_command("-restart")
    main()


def modify_project(title):
    option1 = "change title"
    option2 = "change description"
    option3 = "change location"
    option4 = "change status"
    option5 = "restart"
    options = [option1, option2, option3, option4, option5]
    choice = make_menu(title, options)
    print("\n" + menu_title(options[choice - 1]))
    if choice == 1:
        change_attr("title", "project")
    elif choice == 2:
        change_attr("description", "project")
    elif choice == 3:
        change_attr("location", "project")
    elif choice == 4:
        change_attr("status", "project")
    elif choice == 5:
        global_command("-restart")
    main()


def main():
    option1 = "create new project"
    option2 = "modify existing project"
    option3 = "create new clip"
    option4 = "modify existing clip"
    option5 = "get new episode"
    option6 = "exit"
    options = [option1, option2, option3, option4, option5, option6]
    choice = make_menu("main menu", options)
    if choice == 1:
        print("\n" + menu_title(options[choice - 1]))
        create_new_project()
    elif choice == 2:
        modify_project(option2)
    elif choice == 3:
        print("\n" + menu_title(options[choice - 1]))
        create_new_clip()
    elif choice == 4:
        modify_clip(option4)
    elif choice == 5:
        print("\n" + menu_title(options[choice - 1]))
        create_new_episode()
    elif choice == 6:
        global_command("-exit")
    main()


if __name__ == '__main__':
    scan_files_for_alignment()
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
