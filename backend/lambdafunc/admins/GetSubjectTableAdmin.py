""" Use case:   Should automatically call when the admin opens their homepage. Display all of the subjects, with
                their courses listed in a dropdown.
    Users: Admins
    Type: GET
    Endpoint: ./adminhomepage
    Provide in request:
        Nothing
    TODO:
        Return a list of unique subj/courses
    Response to 200: Dictionary of subjects, with lists of courses
        {
            'subj':  [{
                'subject': 'subj',
                'courseid': 'subj 1001',
                'description': 'Of course',
                'name': 'Intro to Subjects',
                'prereqs': ['subj 1234'],       list of courseids
            }]
            'math': []
        }
    Response otherwise:
        None
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    corsheaders = {
        
    }

    response = client.scan(
        TableName = "Subjects",
        Select='SPECIFIC_ATTRIBUTES',
        AttributesToGet=['subject']
    )
    # list of subjects
    unique_subj = [item['subject']['S'] for item in response['Items']]
    # make unique
    unique_subj = list(set(unique_subj))
    
    # build dictionary to return
    subjdict = {}
    for subj in unique_subj:
        subjdict[subj] = []
        
    # get all of the courses
    all_courses = []
    response = client.scan(
        TableName = "Subjects"
    )
    # go through whole table
    all_courses.extend(response.get('Items', []))
    while 'LastEvaluatedKey' in response:
        response = client.scan(
            TableName= "Subjects",
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        all_courses.extend(response.get('Items', []))

        
    # want to add all of the courses to the dictionary, unless empty
    for course in all_courses:
        subject = course.get('subject', {'S': ''}).get('S', '')
        courseid = course.get('courseid', {'S': ''}).get('S', '')
        if courseid == "empty": continue
        subjdict[subject].append(course)
    
    return {
        'statusCode': 200,
        'headers': corsheaders,
        'body': json.dumps(subjdict)
    }