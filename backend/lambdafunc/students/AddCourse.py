""" Use Case: A student clicks to enroll in a course.
    Users: Students
    Type: POST
    Endpoint: ./studenthomepage/search/courses/sections
    Provide in request:
        Body:
        {
            "CourseID": '',
            "UserID": '',
            "Section": ''
        }
    TODO:
        CHECKS: capacity, prereqs, enrollment, completed
        Update users table for enrollment
        Update courses table for studentlist, enrollment
    Response:
        Strings signifying success or failure
"""

import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    user = event["UserID"]
    course = event["CourseID"]
    section = event["Section"]
    #string to be stored in User table - enrollment
    course_id_section = f"{course}-{section}"
    corsheaders = {
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,OPTIONS,POST",
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
    
    #CHECK: ENROLLMENT, PREREQS, COMPLETED
    #get user information
    user_item = client.get_item(
        TableName='Users',
        Key={
            'Type': {
                'S': "Student",
            },
            'UserID': {
                'S': user        
            }
        }
    )
    #get course info in subj table
    subj = course.split()[0]
    course_item = client.get_item(
        TableName = 'Subjects',
        Key = {
            'subject': {
                'S': subj,
            },
            'courseid': {
                'S': course
            }
        }
    )
    if ('Item' in user_item):
        if ('Item' in course_item):
            #get list of prereqs from course, lists of taken and enrolled courses from user
            prereqs = course_item['Item'].get('Prereqs', {'L': []}).get('L', [])
            taken = user_item['Item'].get('Completed', {'L': []}).get('L', [])
            enrollment = user_item['Item'].get('Enrollment', {'L': []}).get('L', [])
            
            #make lists of strings
            prelist = [item.get('S') for item in prereqs]
            takenlist = [item.get('S') for item in taken]
            clist = [item.get('S') for item in enrollment]
            #PREREQS
            notin = []
            for i in prelist:
                #find missing prereqs
                if i not in takenlist:
                    notin.append(i)
            if len(notin) > 0:
                return {
                    'statusCode': 400,
                    'headers': corsheaders,
                    'body': json.dumps(f'Missing Prereqs: {notin}')
                }
            #TAKEN
            for classes in takenlist:
                #check if already taken
                if course in classes:
                    return {
                        'statusCode': 400,
                        'headers': corsheaders,
                        'body': json.dumps(f'Already completed {course}.')
                    }
            #ALREADY ENROLLED
            for classes in clist:
                #check if enrolled
                if course in classes:
                    return {
                        'statusCode': 400,
                        'headers': corsheaders,
                        'body': json.dumps(f'Already enrolled in {course}.')
                    }
        else:
            #in case course is not found
            return {
                'statusCode': 400,
                'headers': corsheaders,
                'body': json.dumps('Course not found')
            }
    else:
        #in case user is not found in table, should not enter this
        return {
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps('User not found')
        }
        
    #CHECK: CAPACITY
    #get section info from course table
    course_item1 = client.get_item(
        TableName='Courses',
        Key={
            'CourseID': {
                'S': course,
            },
            'Section': {
                'S': section        
            }
        }
    )
    if ('Item' in course_item1):
        #capacity and current enrollment
        cap = course_item1['Item'].get('Capacity', {}).get('N', '0')
        enrollcount = course_item1['Item'].get('Enrollment', {}).get('N', '0')
        if int(enrollcount) >= int(cap):
            #course is full
            return {
                'statusCode': 400,
                'headers': corsheaders,
                'body': json.dumps(f'{course_id_section} is currently full: {enrollcount}/{cap}.')
            }
    else:
        return {
            #should never enter this
            'statusCode': 400,
            'headers': corsheaders,
            'body': json.dumps(f'{course_id_section} not found')
        }
        
        
    #UPDATE TABLES IF PREVIOUS CONDITIONS PASS
    #update section in course table
    response = client.update_item(
        TableName='Courses',
        Key={
            'CourseID': {
                'S': course
            },
            'Section': {
                'S': section
            }
        },
        UpdateExpression='SET Enrollment = Enrollment + :enrollment, StudentList = list_append(StudentList, :userId)',
        ExpressionAttributeValues={
            ':enrollment': {
                'N': '1'                #increment the enrollment
            },
            ':userId': {
                'L': [{'S': user}]      #add user to list of students
            }
        }
    )
    #update users enrollment
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
        UpdateExpression='SET Enrollment = list_append(if_not_exists(Enrollment, :emptyList), :courseIdSection)',
        ExpressionAttributeValues={
            ':emptyList': {
                'L': []
            },
            ':courseIdSection': {
                'L': [{'S': course_id_section}]     #add course-section to student's enrollment list
            }
        }
    )
    return {
        #if everything went well
        'statusCode': 200,
        'headers': corsheaders,
        'body': json.dumps(f'Successfully enrolled in {course_id_section}!')
    }