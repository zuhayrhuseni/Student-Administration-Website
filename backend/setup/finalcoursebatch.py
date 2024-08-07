import json
import random
import string
import boto3

def batchfunction(tname, fname):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tname)

    #Load data from fname
    with open(fname, 'r') as file:
        data = json.load(file)

    #Batch update
    with table.batch_writer() as batch:
        for item in data:
            try:
                batch.put_item(Item=item)
                #print(f"Added item: {item.get('UserID')}")
            except Exception as e:
                print(f"Error adding item: {e}")

    print(f'Batch update completed for table {tname} from {fname}.')

batchfunction("Courses", "resources/All_Classes.json")
batchfunction("Subjects", "resources/All_Subjs.json")