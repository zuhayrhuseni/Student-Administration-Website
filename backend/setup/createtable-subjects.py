import boto3

dynamodb = boto3.client('dynamodb')

def createtable():

    #Define the table name and schema for Courses
    courses_table_name = 'Subjects'
    courses_table = dynamodb.create_table(
        TableName=courses_table_name,
        KeySchema=[
            {'AttributeName': 'subject', 'KeyType': 'HASH'},
            {'AttributeName': 'courseid', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'subject', 'AttributeType': 'S'},
            {'AttributeName': 'courseid', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    #Wait for the table to be created
    courses_table.wait_until_exists()

    print(f'Table {courses_table_name} created successfully.')


if __name__ == "__main__":
    createtable()