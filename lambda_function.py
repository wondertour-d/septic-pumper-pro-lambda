# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#we need to copy AWS env exactly first
import json
import boto3
import requests
from datetime import datetime

print('Loading function')

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb')
document_client = dynamodb.Table('septage-form-results2')

# AWS Lambda client for invoking other Lambda functions
lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    print(f"req.url='{json.dumps(event)}'")

    # Simulating incoming JSON data
    incoming_data = {
        # Include your incoming data structure here
    }

    # Deserialize incoming event
    incoming_form_items = json.loads(json.dumps(event))
    print("Made it past the parse!")

    # Transfer incoming data into variables
    print(f"systemInfo key[]:'{incoming_form_items.get('systemInfo')}'")
    if incoming_form_items.get('systemInfo', {}).get('isProd', False):
        incoming_data = incoming_form_items

    # Define the output array with a length of 100
    output_array = [None] * 100

    # Example of setting values in output_array based on incoming data
    if 'customerInfo' in incoming_data:
        customer_info = incoming_data['customerInfo']
        output_array[0] = customer_info.get('firstName')
        # Continue mapping as needed

    # More processing...
    # Insert more logic here to transform and use the incoming_data as needed

    # Call another Lambda function to hash data
    hashed_data = call_hash_lambda('John', 'Doe', '123 Main St', '555-123-4567', datetime.now().date(),
                                   datetime.now().time())
    print(f"Hashed data: {hashed_data}")

    # Store data in DynamoDB
    store_form_data('2022-03-01', '12:00:00', '555-123-4567', hashed_data['salt'], incoming_data, hashed_data['hash'])

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps('Process completed successfully')
    }


def call_hash_lambda(first_name, last_name, address, phone_number, submit_date, submit_time):
    payload = json.dumps({
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'phone_number': phone_number,
        'submit_date': str(submit_date),
        'submit_time': str(submit_time)
    })
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-east-2:<arn>:function:createUniqueFormHash',
        InvocationType='RequestResponse',
        Payload=payload
    )
    response_payload = json.loads(response['Payload'].read().decode('utf-8'))
    return json.loads(response_payload['body'])


def store_form_data(submit_date, submit_time, phone_number, salt, in_data, hash_value):
    document_client.put_item(
        Item={
            'pumpingdate': submit_date,
            'Time': submit_time,
            'phone_time': f"{phone_number}_{submit_time}",
            'Salt': salt,
            'InputData': in_data,
            'Hash': hash_value
        }
    )
    print('Data stored in DynamoDB')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
