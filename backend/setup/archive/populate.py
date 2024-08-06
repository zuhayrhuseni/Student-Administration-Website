import json
import random
import string

class SharedCourse:
    def __init__(self, prereqs, tlist, subjects):
        #shared information
        self.Name = generate_random_string(10)
        self.CourseID = '{} {}'.format(subjects[random.randint(0, 19)], random.randint(1000, 6400))
        self.Description = generate_random_string(50)
        self.Prereqs = [prereqs[random.randint(0, 19)] for i in range(random.randint(0, 3))]
        #for making sections
        self.posteachers = [tlist[random.randint(0, 39)] for i in range(3)]
        self.count = 0

class User:
    def __init__(self, type, prereqs=[]):
        self.Type = type
        self.UserID = '{}{}'.format(generate_random_stringL(3), random.randint(10000, 24000))
        self.Name = '{} {}'.format(generate_random_string(random.randint(3, 9)), generate_random_string(random.randint(3, 9)))
        self.Password = generate_random_string(15)

        #these should stay empty for admin
        self.taken = []
        if type == 'Student':
            self.taken = [prereqs[random.randint(0, 19)] for i in range(random.randint(0, 4))]
        self.enrolled = []

#functions for random strings
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_stringL(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_random_stringU(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

# Function to generate random schedule data
def generate_random_schedule():
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    schedule = {}
    for day in days_of_week:
        start_time = f"{random.randint(8, 16)}:00"
        end_time = f"{random.randint(8, 16)}:00"
        schedule[day] = f"{start_time}-{end_time}"
    return schedule

#make subjects
subjects = ['{}'.format(generate_random_stringU(random.randint(3,4))) for i in range(20)]

#make prereqs
prereqs = ['{} {}'.format(subjects[random.randint(0, 19)], random.randint(1000, 6400)) for i in range(20)]

#make users
StuList = [User('Student', prereqs) for i in range(1000)]
AdminList = [User('Admin') for i in range(15)]
TeacherList = [User('Teacher') for i in range(40)]

#make list of shared courses
sharedcourses = [SharedCourse(prereqs, TeacherList, subjects) for i in range(75)]

#populate courses
coursepopulation = []
for i in range(300):
    shared = sharedcourses[random.randint(0, 74)]
    shared.count += 1
    teacher = shared.posteachers[random.randint(0, 2)]
    teacher.enrolled.append('{}-{}'.format(shared.CourseID, shared.count))

    course = {
        "CourseID": shared.CourseID,
        "Section": shared.count,
        "Capacity": random.randint(15, 50),
        "Description": shared.Description,
        "Enrollment": 0,
        "Location": '{} {}'.format(generate_random_stringU(4), random.randint(0, 400)),
        "Name": shared.Name,
        "Prerequisites": shared.Prereqs,
        "Schedule": generate_random_schedule(),
        "StudentList": [],
        "TeacherID": teacher.UserID
    }
    coursepopulation.append(course)

#populate users
userpopulation = []
userlist = StuList+AdminList+TeacherList
for user in userlist:
    toadd = {
        "Type": user.Type,
        "UserID": user.UserID,
        "Completed": user.taken,
        "Enrollment": user.enrolled,
        "Name": user.Name,
        "Password": user.Password
    }
    userpopulation.append(toadd)

# Save the course data to a JSON file
with open('courses.json', 'w') as json_file:
    json.dump(coursepopulation, json_file, indent=2)

print("courses.json file created with 100 course examples.")

#with open('users.json', 'w') as json_file:
#    json.dump(userpopulation, json_file, indent=2)

#print("users.json file created with 1000 students, 15 admins, 40 teachers.")