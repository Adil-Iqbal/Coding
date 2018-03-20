import json

data = []

'''
def blank():
    return {
        "name": None,
        "title": ""
    }


# with open("authors", "r") as authors:
#     while True:
#         author = authors.readline()
#         if author == "":
#             break
#         object = blank()
#         object["name"] = author[:-1] if author[-1] == "\n" else author
#         data.append(object)

target_author = "";
q01 = "";
q02 = "";
q03 = "";
q04 = "";
q05 = "";
q06 = "";
q07 = "";
q08 = "";
q09 = "";
q10 = "";
q11 = "";
q12 = "";
q13 = "";
q14 = "";
q15 = "";
q16 = "";
q17 = "";
q18 = "";
q19 = "";
q20 = "";
'''


target_author = "";
q01 = "";
q02 = "";
q03 = "";
q04 = "";
q05 = "";
q06 = "";
q07 = "";
q08 = "";
q09 = "";
q10 = "";
q11 = "";
q12 = "";
q13 = "";
q14 = "";
q15 = "";
q16 = "";
q17 = "";
q18 = "";
q19 = "";
q20 = "";

quotes = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20]

quotes = list(filter(lambda x: x != "", quotes))

message = "Done."

with open("authors.json", "r") as json_file:
    data = json.load(json_file)
    found = False
    for author in data:
        if author["name"] == target_author:
            author["quotes"] = quotes
            found = True
    if not found:
    	message = "Author was not found."

with open("authors.json", "w") as json_file:
    json.dump(data, json_file)

print(message)
