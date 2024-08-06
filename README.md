Student Administration Website
This repository contains the code for a student administration system designed to manage and streamline various administrative tasks for educational institutions.

Features
User Authentication
Course Management
Student Enrollment
Data Management using DynamoDB
RESTful API Endpoints
Project Structure

.
├── backend
│   ├── lambdafunc
│   └── setup
│       ├── archive
│       │   ├── coursebatch.py
│       │   ├── courses.json
│       │   ├── populate.py
│       │   ├── populateold.py
│       │   ├── userbatch.py
│       │   ├── users.json
│       ├── resources
│           ├── EXsubj1234.json
│           ├── EXsubjects.json
│           ├── EXusers.json
│           ├── subjects.json
│           ├── users.json
├── createtable-courses.py
├── createtable-subjects.py
├── createtable-users.py
├── starterPopulation.py
└── procedure.txt

Setup Instructions

Clone the repository:

git clone https://github.com/zuhayrhuseni/Student-Administration-Website.git
cd Student-Administration-Website
Install dependencies:

pip install -r requirements.txt
Set up AWS credentials:
Ensure you have your AWS credentials configured to allow access to DynamoDB.

Create DynamoDB tables:
Run the createtable-*.py scripts to create necessary tables in DynamoDB.

python createtable-courses.py
python createtable-subjects.py
python createtable-users.py
Populate initial data:
Use the starterPopulation.py script to populate the tables with initial data.
python starterPopulation.py
Usage
Running the backend:
Deploy the backend on AWS Lambda or your preferred server.

API Endpoints:
Use the provided scripts and API endpoints to interact with the system.
