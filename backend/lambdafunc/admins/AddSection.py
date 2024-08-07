""" Use Case: An admin adding a section to a database.
    Users: Admins
    Type: POST
    Endpoint: ./adminhomepage/section
    Provide in request:
        Body:
        {
            
        }
    TODO:
        Validate input data (e.g., check for missing fields, validate CourseID format).
        Check if the course already exists in the database.
        Add the new course to the Courses table.
    Response:
        Strings signifying success or failure
"""

import json
import boto3


client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # extract data from the request body
    course_id = event.get("CourseID")
    capacity = event.get("Capacity")
    section = event.get("Section")
    location = event.get("Location")
    schedule = event.get("Schedule")
    teacher_id = event.get("TeacherID")
    teacher_name = event.get("TeacherName")

    # ensure all required fields are present
    if not all([course_id, capacity, section, location, schedule, teacher_id]):
        return response(400, 'Missing required course details')

    # Check if the course already exists
    existing_course = client.get_item(
        TableName='Courses',
        Key={
            'CourseID': {'S': course_id},
            'Section': {'S': section}
        }
    )

    if 'Item' in existing_course:
        return response(400, f'Course {course_id} Section {section} already exists')

    # Add the new course to the Courses table
    client.put_item(
        TableName='Courses',
        Item={
            'CourseID': {'S': course_id},
            'Section': {'S': str(section)},
            'Capacity': {'N': str(capacity)},
            'Enrollment': {'N': '0'},
            'Location': {'S': location},
            'Schedule': {'M': schedule},
            'TeacherID': {'S': teacher_id},
            'TeacherName': {'S': teacher_name},
            'StudentList': {'L': []}  # Initializing StudentList as an empty list
        }
    )

    return response(200, f'Course {course_id} Section {section} added successfully')

def response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {
          "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
          "Access-Control-Allow-Methods": "OPTIONS,POST",
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json"
        }

    }