import json

filePath = "utils/data/userData.json"
# initialize


with open(filePath, 'r') as json_file:
    userData = json.load(json_file)

def printUserData(name):
    for user in userData['users']:
        if user['name'] == name:
            # return user
            print("Name: {name}\n\t")

    return -1

print(printUserData('root'))