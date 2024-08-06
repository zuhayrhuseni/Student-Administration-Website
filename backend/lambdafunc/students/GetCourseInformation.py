""" Use case:   When a student clicks on a section they are assigned to in order to find more information.
    Users: Students
    Type: GET
    Endpoint: ./studenthomepage/enrollment/courseinfo
    Provide in request:
        Query String:
            course-id-section=___
    TODO:
        Query course table for more information on this section
    Response to 200:
        {
            'Location': '',
            'Schedule': {
                'Monday': '',
                'Wednesday': '',
                'Friday': ''
            }
            'Teacher': 'Name'
        }
    Response otherwise:
        String detailing error
"""
#example of authorization can be found in bottom of GetCourseInfoTeacher.py

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    course_id_section = event["course-id-section"]
    split = course_id_section.split('-')
    courseid = split[0]
    section = split[1]
    corsheaders = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    #find section
    course_item = client.get_item(
        TableName='Courses',
        Key={
            'CourseID': {
                'S': courseid,
            },
            'Section': {
                'N': section
            }
        }
    )
    if ('Item' in course_item):
        #get items to return
        location = course_item['Item'].get('Location', {'S': ''}).get('S', '')
        schedule = course_item['Item'].get('Schedule', {'M': {}}).get('M', '')
        for day in schedule:
            schedule[day] = schedule[day].get('S', '')
        teacher = course_item['Item'].get('TeacherName', {'S': ''}).get('S', '')
        result = {}
        result['Location'] = location
        result['Schedule'] = schedule
        result['TeacherName'] = teacher
        
        return {
            'statusCode': 200,
            'headers': corsheaders,
            'body': result
        }
        
    else:
        return {
            #should not reach this point
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'Course not found')
        }