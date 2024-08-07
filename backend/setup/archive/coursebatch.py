import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Courses')

#Load data
with open('courses.json', 'r') as file:
    data = json.load(file)

#Batch update
with table.batch_writer() as batch:
    for item in data:
        try:
            batch.put_item(Item=item)
            #print(f"Added item: {item.get('CourseID')} - {item.get('Section')}")
        except Exception as e:
            print(f"Error adding item: {e}")

print(f'Batch update completed for Courses.')