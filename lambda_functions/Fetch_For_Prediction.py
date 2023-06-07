import boto3
from datetime import datetime
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('date_power_data')

    # Query DynamoDB for all records
    response = table.scan()

    # Create a dictionary to store the power values for each day
    power_dict = {}

    # Populate the dictionary with the power values from DynamoDB
    for item in response['Items']:
        date_str = item['date']
        power = float(item.get('power', 0))  # If power attribute is missing, default to zero
        power_dict[date_str] = power

    response = {
        'statusCode': 200,
        'body': json.dumps({"values": power_dict})
    }

    return response
