# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.




#we need to copy AWS env exactly first
import json
import boto3
import requests
from datetime import datetime
import logging

print('Loading function')

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb')
document_client = dynamodb.Table('septage-form-results2')

# AWS Lambda client for invoking other Lambda functions
lambda_client = boto3.client('lambda')

print("inside lambda now")

def lambda_handler(event, context):
    print(f"req.url='{json.dumps(event)}'")

    try:
        # Your code here
        logging.info("Handler started successfully")
    except Exception as e:
        logging.error(f"Error in handler: {str(e)}")
        raise e

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

        # Example: Define output data structure with default values or structures
        output_data = {
            'submission': {
                'first_name': None,
                'last_name': None,
                'address': None,
                'pumping_date': None,
                'county': None,
                'township': None,
                'phone_full': None,
                'email': None,
                'customer_type': None,
                'tank_condition': None,
                'material_type': [],
                'tank_type': None,
                'total_gallons_pumped': 0,
                'technician_name': None,
                'company_phone': None,
                'company_name': None
            }
        }

        # Example mappings from incoming data to output structure
        # Mapping 10 example fields
        customer_info = incoming_data.get('customerInfo', {})
        tank_system = incoming_data.get('tankSystem', {})
        general_info = incoming_data.get('generalInfo', {})

        output_data['submission']['first_name'] = customer_info.get('firstName', 'Empty')
        output_data['submission']['last_name'] = customer_info.get('lastName', 'Empty')
        output_data['submission']['address'] = customer_info.get('address','Empty')
        output_data['submission']['county'] = customer_info.get('county','Empty')
        output_data['submission']['township'] = customer_info.get('township','Empty')
        output_data['submission']['phone_full'] = customer_info.get('phone','Empty')
        output_data['submission']['email'] = customer_info.get('email','Empty')
        output_data['submission']['customer_type'] = customer_info.get('customerType','Empty')


        output_data['submission']['technician_name'] = general_info.get('technicianName','Empty')
        output_data['submission']['company_phone'] = general_info.get('companyPhone','Empty')
        output_data['submission']['company_name'] = general_info.get('septageHaulingCompany','Empty')


        # Processing dates for example
        if 'pumpingDate' in customer_info:
            date_str = customer_info['pumpingDate']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            output_data['submission']['pumping_date'] = {
                'day': date_obj.day,
                'month': date_obj.month,
                'year': date_obj.year
            }

        # Example of aggregating tank data
        if 'tanks' in tank_system:
            #



            total_gallons = sum(int(tank.get('gallonsPumped', 0)) for tank in tank_system['tanks'])
            output_data['submission']['total_gallons_pumped'] = total_gallons

        # Return or further process `output_data`
        return {
            'statusCode': 200,
            'body': json.dumps(output_data)
        }


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
