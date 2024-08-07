""" Use Case: An admin adding a subject to a database.
    Users: Admins
    Type: POST
    Endpoint: ./adminhomepage
    Provide in request:
        Body:
        {
            "CourseID": '',
            "UserID": '',
            "Section": N
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
    subject = event.get("subject")

    # Get the value of the "courseid" key from the event dictionary
    courseid = event.get("courseid")
    description = event.get("Description")
    name = event.get("Name")
    prereqs = event.get("Prereqs", [])

    if not all([subject, courseid, description, name]):
        return response(400, 'Missing required subject details')

    existing_subject = client.get_item(
        TableName='Subjects',
        Key={
            'subject': {'S': subject},
            'courseid': {'S': courseid}
        }
    )

    if 'Item' in existing_subject:
        return response(400, f'Subject {subject} with CourseID {courseid} already exists')

    
    client.put_item(
        TableName='Subjects',
        Item={
            'subject': {'S': subject},
            'courseid': {'S': courseid},
            'Description': {'S': description},
            'Name': {'S': name},
            'Prereqs': {'L': [{'S': prereq} for prereq in prereqs]}
        }
    )
    return response(200, f'Subject {subject} with CourseID {courseid} added successfully')

def response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
