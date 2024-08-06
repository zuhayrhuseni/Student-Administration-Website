import json
import boto3

# Initialize a session using Amazon DynamoDB.
dynamodb = boto3.resource('dynamodb')

# Define the table name.
table_name = 'Users'

# Get a reference to the DynamoDB table.
table = dynamodb.Table(table_name)

# Load data from the "courses.json" file
with open('users.json', 'r') as file:
    data = json.load(file)

# Batch update the DynamoDB table with items from the JSON file
with table.batch_writer() as batch:
    for item in data:
        try:
            batch.put_item(Item=item)
            #print(f"Added item: {item.get('UserID')}")
        except Exception as e:
            print(f"Error adding item: {e}")

print(f'Batch update completed for table {table_name}.')