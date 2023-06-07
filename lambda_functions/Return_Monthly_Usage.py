import boto3
from datetime import datetime, timedelta
import decimal
import json

def default_json(t):
    return f'{t}'

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('date_power_data')

    # Get the current month and year
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year
    
    # # Calculate the start and end dates for the current month
    start_date = datetime(current_year, current_month, 1)
    end_date = now.strftime("%d-%m-%Y")
#start_date + timedelta(days=30)  # Add extra days to include the next month
    
    start_date = start_date.strftime("%d-%m-%y")
    # end_date = end_date.strftime("%d-%m-%y")
    
    # start_date = "01-05-23"
    # end_date = "31-05-23"
    
    # Query DynamoDB for records within the current month
    response = table.scan(
        FilterExpression="#date BETWEEN :start_date AND :end_date",
        ExpressionAttributeNames={"#date": "date"},
        ExpressionAttributeValues={
            ":start_date": start_date,#.strftime("%d-%m-%y"),
            ":end_date":  end_date,#.strftime("%d-%m-%y")
        }
    )
    
    # Create a dictionary to store the power values for each day of the month
    power_dict = {}
    
    # Initialize the dictionary with zero values for each day
    for day in range(1, 32):
        power_dict[day] = 0
    
    # Populate the dictionary with the power values from DynamoDB
    for item in response['Items']:
        date_str = item['date']
        power = item.get('power', 0)  # If power attribute is missing, default to zero
        day = int(date_str.split('-')[0])
        power_dict[day] = int(power)
    
    # Sort the dictionary by day and convert it to a list of values
    sorted_power = [power_dict[day] for day in sorted(power_dict.keys())]
    
    # serial_string = ""
    
    # for item in sorted_power:
    #     serial_string = str(item)+" "
    
    # serial_string = serial_string.strip()
    
    response = {
        'statusCode': 200,
        'body': json.dumps({"values":sorted_power})
    }
    
    return response
