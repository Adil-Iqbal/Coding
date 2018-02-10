import requests
import json

url = "https://www.googleapis.com/youtube/v3/search"
api_key = "AIzaSyBoVWZevLKCgLn_v-KNyT7gt3fsr_JdA4M"
parameters = {"part": "snippet",
              "channelId": "UCFKDEp9si4RmHFWJW1vYsMA",
              "q": "",
              "type": "video",
              "key": api_key,
              "maxResults": 1
              }

with open("episode_ids_list.txt", "w") as file:
    for x in range(105, 499):
        parameters["q"] = "Etho Plays Minecraft - Episode " + str(x)
        result = requests.request(method="get", url=url, params=parameters)
        j_result = json.loads(result.text)
        try:
            file.writelines(j_result['items'][0]['id']['videoId'] + "\n")
        except IndexError:
            err_msg = "Skipping episode " + str(x) + "."
            print(err_msg)
            file.writelines(err_msg + "\n")
    else:
        print("Done!")
