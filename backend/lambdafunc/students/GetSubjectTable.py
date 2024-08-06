""" Use case:   Should automatically call when a student opens the filter/search page,
                or the admin opens their homepage. Display all of the subjects, with
                their courses listed in a dropdown.
    Users: Students, Admins
    Type: GET
    Endpoint: ./adminhomepage, ./studenthomepage/search
    Provide in request:
        Nothing
    TODO:
        Return a list of unique subj/courses
    Response to 200: Dictionary of subjects, with lists of courses
        [
            {'SUBJ':  [{
                'subject': 'SUBJ',
                'courseid': 'SUBJ 1001',
                'Description': 'Of course'
                'Name': 'Intro to Subjects',
                'Prereqs': ['SUBJ 1234'],       list of courseids
            }]}
            {'MATH': []}
        ]
    Response otherwise:
        None
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    corsheaders = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    response = client.scan(
        TableName = "Subjects",
        Select='SPECIFIC_ATTRIBUTES',
        AttributesToGet=['subject']
    )
    #list of subjects
    unique_subj = [item['subject']['S'] for item in response['Items']]
    #make unique
    unique_subj = list(set(unique_subj))
    
    #build dictionary to return
    subjdict = {}
    for subj in unique_subj:
        subjdict[subj] = []
        
    #get all of the courses
    all_courses = []
    response = client.scan(
        TableName = "Subjects"
    )
    #go through whole table
    all_courses.extend(response.get('Items', []))
    while 'LastEvaluatedKey' in response:
        response = client.scan(
            TableName= "Subjects",
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        all_courses.extend(response.get('Items', []))
        
    #want to add all of the courses to the dictionary, unless empty
    #also making body nicer for front end
    for course in all_courses:
        cid = course.get('courseid', {'S': ''}).get('S', '')
        subject = course.get('subject', {'S': ''}).get('S', '')
        if cid == "empty": continue
    
        prereqs = course.get('Prereqs', {'L': []}).get('L', [])
        prelist = []
        for i in prereqs:
            prelist.append(i["S"])
    
        coursedict = {
            'subject': subject,
            'courseid': cid,
            'description': course.get('Description', {'S': ''}).get('S', ''),
            'name': course.get('Name', {'S': ''}).get('S', ''),
            'prereqs': sorted(prelist)
        }
    
        #adding course dictionaries to subject dictionaries
        subjdict[subject].append(coursedict)
        #sorting the course dictionaries by courseid
        subjdict[subject] = sorted(subjdict[subject], key=lambda x: x['courseid'])
        
        #make a sorted list to return sorted by subjects
        retlist = []
        for key in subjdict:
            retlist.append({key: subjdict[key]})
        retlist = sorted(retlist, key=lambda x: list(x.keys())[0])
    
    return {
        'statusCode': 200,
        'headers': corsheaders,
        'body': retlist
    }