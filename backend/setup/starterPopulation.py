import json
import random
import string
import boto3

""" The purpose of this is to populate the tables with starting information. 
    An example will be loaded into subjects along with a few empty subjects. 
    All users will be created (1000 students, 40 teachers, 15 admins).
        With 3 examples: pro12003, std20001, adi16007
    An example course will be loaded into courses - SUBJ 1234-1
    RUN THIS TO POPULATE TABLES WITH RESOURCES
"""

def batchfunction(tname, fname):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tname)

    #Load data from fname
    with open(fname, 'r') as file:
        data = json.load(file)

    #Batch update
    with table.batch_writer() as batch:
        for item in data:
            try:
                batch.put_item(Item=item)
                #print(f"Added item: {item.get('UserID')}")
            except Exception as e:
                print(f"Error adding item: {e}")

    print(f'Batch update completed for table {tname} from {fname}.')



"""class User:
    def __init__(self, type):
        self.Type = type
        self.UserID = '{}{}'.format(generate_random_stringL(3), random.randint(10000, 24000))
        self.Name = '{} {}'.format(generate_random_string(random.randint(3, 9)), generate_random_string(random.randint(3, 9)))
        self.Password = generate_random_string(15)

        #these should stay empty for admin
        if type == 'Student':
            self.taken = []
            self.enrolled = []
        if type == 'Teacher':
            self.enrolled = []

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_stringL(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_random_stringU(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

subjlist = ["SUBJ", "MATH", "DDB", "CSE", "ANTH"]

StuList = [User('Student') for i in range(1000)]
AdminList = [User('Admin') for i in range(15)]
TeacherList = [User('Teacher') for i in range(40)]

userpopulation = []
for user in StuList:
    toadd = {
        "Type": user.Type,
        "UserID": user.UserID,
        "Completed": user.taken,
        "Enrollment": user.enrolled,
        "Name": user.Name,
        "Password": user.Password
    }
    userpopulation.append(toadd)

for user in AdminList:
    toadd = {
        "Type": user.Type,
        "UserID": user.UserID,
        "Name": user.Name,
        "Password": user.Password
    }
    userpopulation.append(toadd)

for user in TeacherList:
    toadd = {
        "Type": user.Type,
        "UserID": user.UserID,
        "Enrollment": user.enrolled,
        "Name": user.Name,
        "Password": user.Password
    }
    userpopulation.append(toadd)

with open('resources/users.json', 'w') as json_file:
    json.dump(userpopulation, json_file, indent=2)

print("users.json file created with 1000 student examples.")

subjpopulation = []
for subj in subjlist:
    toadd = {
        "subject": subj,
        "courseid": "empty",
    }
    subjpopulation.append(toadd)

with open('resources/subjects.json', 'w') as json_file:
    json.dump(subjpopulation, json_file, indent=2)

print("subjects.json file created with starter subjects.")"""

#batchfunction("Subjects", "resources/EXsubjects.json")
#batchfunction("Subjects", "resources/subjects.json")
batchfunction("Courses", "resources/EXsubj1234.json")
#batchfunction("Users", "resources/EXusers.json")
#batchfunction("Users", "resources/users.json")