import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name="us-east-1")

def createtable():

    # Define the table name and schema for the Users table.
    users_table_name = 'Users'
    users_table = dynamodb.create_table(
        TableName=users_table_name,
        KeySchema=[
            {'AttributeName': 'Type', 'KeyType': 'HASH'},
            {'AttributeName': 'UserID', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'Type', 'AttributeType': 'S'},
            {'AttributeName': 'UserID', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait for the table to be created.
    users_table.wait_until_exists()

    print(f'Table {users_table_name} created successfully.')


if __name__ == "__main__":
    createtable()