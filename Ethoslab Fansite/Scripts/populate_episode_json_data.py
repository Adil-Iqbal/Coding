import requests
import json
from pprint import pprint
import traceback

"""This script is used to populate a JSON file with formatted Episode data."""


def get_episode_num(string):
    """Returns the episode number as an integer."""
    for i, char in enumerate(string):
        if char == ":":
            return int(string[i - 3:i])


def to_seconds(string):
    """Returns number of seconds as an integer."""
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
            except:
                traceback.print_exc()
                return original_string
            num = ""
    return seconds


url = "https://www.googleapis.com/youtube/v3/videos"
api_key = "AIzaSyBoVWZevLKCgLn_v-KNyT7gt3fsr_JdA4M"
#
# with open("episode_ids_list.txt", "r") as id_list:
#     for i in range(303):
#         parameters = {"part": "snippet,contentDetails",
#                       "id": id_list.readline(),
#                       "key": api_key,
#                       }
#         result = requests.request(method="get", url=url, params=parameters)
#         j_result = json.loads(result.text)
#         try:
#             episode_dict = {
#                 "id": 0,
#                 "type": "episode",
#                 "youtube_id": j_result['items'][0]['id'],
#                 "title": j_result['items'][0]['snippet']['title'],
#                 "episode": get_episode_num(j_result['items'][0]['snippet']['title']),
#                 "description": j_result['items'][0]['snippet']['description'],
#                 "published_at": j_result['items'][0]['snippet']['publishedAt'],
#                 "duration": to_seconds(j_result['items'][0]['contentDetails']['duration']),
#                 "media": j_result['items'][0]['snippet']['thumbnails'],
#                 "associated_clips": [],
#                 "curation": {
#                     "curated_time": 0,
#                     "percentage": 0.0
#                 }
#             }
#             episode_dict["id"] = episode_dict["episode"] - 105
#             with open("episodes.json") as j_data:
#                 d_data = json.load(j_data)
#             d_data.append(episode_dict)
#             with open("episodes.json", "w") as j_data:
#                 json.dump(d_data, j_data)
#         except:
#             traceback.print_exc()
#             pprint(j_result['items'][0])
#             break
#     else:
#         print("Done!")

# *** Code used to find common errors in insertions to all_episodes list.
# def scan_episodes_file_for_common_errors():
#     with open("episodes.json", "r") as j_data:
#         print("Scanning 'episodes.json' for common issues...")
#         d_data = json.load(j_data)
#         prev_ep = -1
#         for i, episode in enumerate(d_data):
#             if type(episode["duration"]) == str:
#                 print(
#                     "Duration string (" + episode["duration"] + ") detected at... Index: " + str(i) + ", Episode ID:" + str(
#                         episode["id"]))
#             if prev_ep > episode["id"]:
#                 print("Possibly repeated episode insertion at... Index: " + str(i) + ", Episode ID:" + str(episode["id"]))
#             elif not ((episode["id"] - prev_ep) == 1):
#                 print("Possible skip of length " + str(episode["id"] - prev_ep) + " detected at... Index: " + str(
#                     i) + ", Episode ID:" + str(episode["id"]))
#             else:
#                 prev_ep = episode["id"]
#         else:
#             print("Scan concluded.")
#
# scan_episodes_file_for_common_errors()


from random import randint
number_list = [randint(1, 30) for i in range(80)]

print(number_list)

for k in range(1, len(number_list)):
    for i in range(0, len(number_list)-k):
        if number_list[i] > number_list[i+1]:
            number_list[i], number_list[i + 1] = number_list[i + 1], number_list[i]

print(number_list)