""" Use case:   When a teacher clicks on a section they are assigned to in order to find more information.
    Users: Teachers
    Type: GET
    Endpoint: ./teacherhomepage/enrollment/courseinfo
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
            'StudentList': ['UserID']
        }
    Response otherwise:
        String detailing error
"""
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
    #find course
    course_item = client.get_item(
        TableName='Courses',
        Key={
            'CourseID': {
                'S': courseid,
            },
            'Section': {
                'S': section
            }
        }
    )
    if ('Item' in course_item):
        #get items to return
        location = course_item['Item'].get('Location', {'S': ''}).get('S', '')
        schedule = course_item['Item'].get('Schedule', {'M': {}}).get('M', {})
        for day in schedule:
            schedule[day] = schedule[day].get('S', '')
        SList = course_item['Item'].get('StudentList', {'L': []}).get('L', [])
        studentlist = []
        for student in SList:
            studentlist.append(student.get('S', ''))
        result = {}
        result['Location'] = location
        result['Schedule'] = schedule
        result['StudentList'] = studentlist
        return {
            'statusCode': 200,
            'headers': corsheaders,
            'body': json.dumps(result)
        }
        
    else:
        return {
            #should not reach this point
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'Course not found')
        }
    

#EXTRA
"""authorization - could be done in later step
#CHECK FOR AUTHORIZATION - make sure user with that type exists
    user_item = client.get_item(
        TableName='Users',
        Key={
            'Type': {
                'S': 'Teacher',
            },
            'UserID': {
                'S': userid    
            }
        }
    )
    
    if ('Item' not in user_item):
        return {
            'statusCode': 400,
            'body': json.dumps(f'Incorrect Authorization')
        }
        """