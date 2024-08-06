""" Use case:   In search, students will click on a course in order to view
                the sections of that course. Admins will do the same.
    Users: Students, Admins
    Type: GET
    Endpoint: ./studenthomepage/courses/sections, ./adminhomepage/courses/sections
    Provide in request:
        Query String:
            CourseID=___
    TODO:
        Query course table for courseid
        Return all sections of the course
    Respons to 200: List of sections (dictionaries)
        [
            {
                'Enrollment': N,
                'Capacity': N,
                'Location': '',
                'TeacherName': '',
                'CourseID': '',
                'Schedule': {
                    'Monday': '',
                    'Tuesday': '',
                    'Thursday': ''
                },
                'Section': 1
            },
            {Section 2},...
        ]
        
    Response otherwise:
        String detailing error
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    courseid = event["CourseID"]
    corsheaders = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,OPTIONS,POST",
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
    
    #get sections
    response = client.query(
        TableName = "Courses",
        KeyConditionExpression='#courseid = :val',
        ExpressionAttributeNames={
                '#courseid': 'CourseID', 
                '#sec': 'Section', 
                '#enr': 'Enrollment', 
                '#cap': 'Capacity', 
                '#loc': 'Location',
                '#sched': 'Schedule',
                '#teachname': 'TeacherName'
        },
        ExpressionAttributeValues={':val': {'S': courseid}},
        ProjectionExpression = '#courseid, #sec, #enr, #cap, #loc, #sched, #teachname'
    )
    
    #converting result to something usable by frontend
    sectionsList = response.get('Items', [])
    for section in sectionsList:
        section['CourseID'] = section.get('CourseID', '').get('S', '')
        section['Section'] = section.get('Section', '').get('N', '')
        section['Enrollment'] = section.get('Enrollment', '').get('N', '')
        section['Capacity'] = section.get('Capacity', '').get('N', '')
        section['Location'] = section.get('Location', '').get('S', '')
        section['Schedule'] = section.get('Schedule', '').get('M', '')
        for day in section['Schedule']:
            section['Schedule'][day] = section['Schedule'][day].get('S', '')
        section['TeacherName'] = section.get('TeacherName', '').get('S', '')

    if len(sectionsList) == 0:
        return {
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'No available sections')
        }
    return {
        'statusCode': 200,
        'headers': corsheaders,
        'body': sectionsList
    }