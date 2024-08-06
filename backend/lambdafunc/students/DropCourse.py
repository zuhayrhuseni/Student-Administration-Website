""" Use Case: A student clicks to drop a course from the list they are enrolled in.
    Users: Students
    Type: POST
    Endpoint: ./studenthomepage/enrollment
    Provide in request:
        Body:
        {
            "course-id-section": '',
            "UserID": ''
        }
    TODO:
        Get information from user table and update.
        Get information from course table and update.
    Response:
        Strings signifying success or failure
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    course_id_section = event["course_id_section"]
    cis = course_id_section.split('-')
    courseid = cis[0]
    section = cis[1]
    user = event["UserID"]
    corsheaders = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,OPTIONS,POST",
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    #find user
    user_item = client.get_item(
            TableName = 'Users',
            Key={
            'Type': {
                'S': "Student"
            },
            'UserID': {
                'S': user
            }
        }
    )
    if "Item" in user_item:
            #get list of enrollment
            courselist = user_item['Item'].get('Enrollment', {'L': []}).get('L', [])
            #make new enrollment list - without course
            course_list = [classes for classes in courselist if classes['S'] != course_id_section]
            #if nothing changed, they were not enrolled in course
            if courselist == course_list:
                return {
                    'statusCode': 400,
                    'headers': corsheaders,
                    'body': json.dumps(f'Not enrolled in {course_id_section}')
                }
    else:
        return {
            #should never enter this
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'{user} not found')
        }
    #update user
    response2 = client.update_item(
        TableName='Users',
        Key={
            'Type': {
                'S': "Student",
            },
            'UserID': {
                'S': user        
            }
        },
        UpdateExpression='SET Enrollment = :enrollment',
        ExpressionAttributeValues={
            ':enrollment': {
                'L': course_list
            }
        }
    )
    
    #find course
    course_item = client.get_item(
            TableName = 'Courses',
            Key={
            'CourseID': {
                'S': courseid
            },
            'Section': {
                'N': section
            }
        }
    )
    if "Item" in course_item:
        #get information to change
        studentlist = course_item['Item'].get('StudentList', {'L': []}).get('L', [])
        #enrollment = course_item['Item'].get('Enrollment', {}).get('N', '0')
        student_list = [student for student in studentlist if student['S'] != user]
        enrollment = len(student_list)
    else:
        return {
            #should never enter this
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'{course_id_section} not found')
        }
            
    #update course
    response = client.update_item(
        TableName='Courses',
        Key={
            'CourseID': {
                'S': courseid
            },
            'Section': {
                'N': section
            }
        },
        UpdateExpression='SET Enrollment = :enrollment, StudentList = :student_list',
        ExpressionAttributeValues={
            ':enrollment': {
                'N': str(enrollment)
            },
            ':student_list': {
                    'L': student_list
            }
        }
    )

    return {
        'statusCode': 200,
        'headers': corsheaders,
        'body': json.dumps(f'Successfully dropped {course_id_section}!')
    }