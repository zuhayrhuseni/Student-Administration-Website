import boto3

dynamodb = boto3.client('dynamodb')

def createtable():

    #Define the table name and schema for the Courses table.
    courses_table_name = 'Courses'
    courses_table = dynamodb.create_table(
        TableName=courses_table_name,
        KeySchema=[
            {'AttributeName': 'CourseID', 'KeyType': 'HASH'},
            {'AttributeName': 'Section', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'CourseID', 'AttributeType': 'S'},
            {'AttributeName': 'Section', 'AttributeType': 'N'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    #Wait for the table to be created.
    courses_table.wait_until_exists()

    print(f'Table {courses_table_name} created successfully.')


if __name__ == "__main__":
    createtable()