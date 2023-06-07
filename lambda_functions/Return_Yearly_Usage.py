import boto3
from collections import defaultdict
import json

def lambda_handler(event, context):
    # Set up the DynamoDB client
    dynamodb = boto3.client('dynamodb')
    table_name = 'date_power_data'

    total = []
    
    scan_params = {
        'TableName': table_name
    }

    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        
        total_power = 0
        
        response = dynamodb.scan(**scan_params)
        
        print(response)
        
        for item in response["Items"]:
            date = item['date']['S']
            power = item['power']['N']
            
            if date.split("-")[1] == month:
                total_power+=float(power)
        
        total.append(float(total_power))
        
    
    # Return the response dictionary as the Lambda function result
    return {
        'statusCode': 200,
        'body': json.dumps({"values":total})
    }