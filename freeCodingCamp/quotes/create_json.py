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


target_author = "Martin Luther King Jr.";
q01 = "May I stress the need for courageous, intelligent, and dedicated leadership... Leaders of sound integrity. Leaders not in love with publicity, but in love with justice. Leaders not in love with money, but in love with humanity. Leaders who can subject their particular egos to the greatness of the cause.";
q02 = "The richer we have become materially, the poorer we become morally and spiritually. We have learned to fly in the air like birds and swim in the sea like fish, but we have not learned the simple art of living together as brothers.";
q03 = "The ultimate measure of a man is not where he stands in moments of comfort and convenience, but where he stands at times of challenge and controversy. Nothing worthwhile is easy. Your ability to overcome unfavorable situations will provide you with time to demonstrate your true strength and determination for success. ";
q04 = "In the End, we will remember not the words of our enemies, but the silence of our friends.";
q05 = "If you can't fly then run, if you can't run then walk, if you can't walk then crawl, but whatever you do you have to keep moving forward.";
q06 = "We may have all come on different ships, but we're in the same boat now.";
q07 = "Forgiveness is not an occasional act, it is a constant attitude.";
q08 = "Commit yourself to the noble struggle for human rights. You will make a greater person of yourself, a greater nation of your country and a finer world to live in.";
q09 = "Call it democracy, or call it democratic socialism, but there must be a better distribution of wealth within this country for all God's children.";
q10 = "Never forget that everything Hitler did in Germany was legal.";
q11 = "An individual has not started living until he can rise above the narrow confines of his individualistic concerns to the broader concerns of all humanity.";
q12 = "We all too often have socialism for the rich and rugged free market capitalism for the poor.";
q13 = "Change does not roll in on the wheels of inevitability, but comes through continuous struggle.";
q14 = "Life's piano can only produce melodies of brotherhood when it is recognized that the black keys are as basic, necessary and beautiful as the white keys.";
q15 = "Men often hate each other because they fear each other; they fear each other because they don't know each other; they don't know each other because they can not communicate; they can not communicate because they are separated.";
q16 = "Forgiveness does not mean ignoring what has been done or putting a false label on an evil act. It means, rather, that the evil act no longer remains as a barrier to the relationship. Forgiveness is a catalyst creating the atmosphere necessary for a fresh start and a new beginning.";
q17 = "It is a cruel injustice to tell a bootless man to pull himself up by his bootstraps.";
q18 = "I may not be the man I want to be; I may not be the man I ought to be; I may not be the man I could be; I may not be the man I truly can be; but praise God, I'm not the man I once was";
q19 = "Faith is taking the first step even when you don't see the whole staircase.";
q20 = "The function of education is to teach one to think intensively and to think critically. Intelligence plus character - that is the goal...";

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
