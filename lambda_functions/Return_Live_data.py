import boto3
from collections import defaultdict
import json

def lambda_handler(event, context):
    # Set up the DynamoDB client
    dynamodb = boto3.client('dynamodb')
    table_name = 'live_data_table'

    total = []
    
    scan_params = {
        'TableName': table_name
    }
    
    response = dynamodb.scan(**scan_params)
    
    voltage_main = 0
    current_main = 0
    power_main = 0
    
    for item in response["Items"]:
        voltage_main = float(item["live_voltage_main"]["N"])
        current_main = float(item["live_current_main"]["N"])
        power_main = float(item["live_power_main"]["N"])
        main_status = float(item['main_status']["N"])
        dev1_status = float(item["dev1_status"]["N"])
        dev2_status = float(item["dev2_status"]["N"])
    
    # Return the response dictionary as the Lambda function result
    return {
        'statusCode': 200,
        'body': json.dumps({"live_voltage_main":voltage_main,"live_current_main":current_main,"live_power_main":power_main,"main_status":main_status,"dev1_status":dev1_status,"dev2_status":dev2_status})
    }