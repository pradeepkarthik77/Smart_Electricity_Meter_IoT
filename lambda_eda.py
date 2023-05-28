import boto3
import datetime
import json

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')
iot_client = boto3.client('iot-data')


def lambda_handler(event, context):
    # Extract data from the event
    current_main = event['current_main']
    voltage_main = event['voltage_main']
    power_main = event['power_main']
    
    current_dev1 = event['current_dev1']
    voltage_dev1 = event['voltage_dev1']
    power_dev1 = event['power_dev1']
    
    current_dev2 = event['current_dev2']
    voltage_dev2 = event['voltage_dev2']
    power_dev2 = event['power_dev2']
    
    if(voltage_main>300):
        message_text = "Hi,\nI have found that the voltage supply is abnormally high({0} volts) and for safety, I have suspended the current supply to our home. If you find this abnormal, Visit the website to turn the power back on.\nThanks.".format(
            str(voltage_main)
        )
        
        subject = "Re: Abnormal Voltage spike found!!!"

        # Publish the formatted message
        response = sns.publish(
                TopicArn = event['notify_topic_arn'],
                Message = message_text,
                Subject = subject
            )
        
        topic = "esp32/sub"
        message = {"message": "mainoff"}
        
        payloader = json.dumps(message)
        
        response = iot_client.publish(
        topic='esp32/sub',
        payload= payloader
        )
    
    # Get the current date and time
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H:%M:%S")
    
    total = date+" "+time
    
    dynamodb.put_item(
        TableName='meter_data',
        Item={
            'current_main': {'N': str(current_main)},
            'voltage_main': {'N':str(voltage_main)},
            'power_main': {'N': str(power_main)},
            'current_dev1': {'N': str(current_dev1)},
            'voltage_dev1': {'N':str(voltage_dev1)},
            'power_dev1': {'N': str(power_dev1)},
            'current_dev2': {'N': str(current_dev2)},
            'voltage_dev2': {'N':str(voltage_dev2)},
            'power_dev2': {'N': str(power_dev2)},
            'date': {'S': date},
            'time': {'S': time},
            'date_time': {'S': total}
        }
    )
    
    main_stats = 0
    dev1_stats = 0
    dev2_stats = 0
    
    if voltage_main<50:
        main_stats = 0
    else:
        main_stats = 1
    
    if voltage_dev1<50:
        dev1_stats = 0
    else:
        dev1_stats = 1
    
    if voltage_dev2<50:
        dev2_stats = 0
    else:
        dev2_stats = 1
    
    # enter logic to change functions to incorporate dev1 and dev2
    
    table_name = 'live_data_table'
    primary_key = {'entry_no': {'N': '1'}}
    
    # Create an UpdateItemRequest object
    update_item_request = {
        'TableName': table_name,
        'Key': primary_key,
        'UpdateExpression': 'SET live_current_main = :current_main, live_voltage_main = :voltage_main, live_power_main = :power_main, live_voltage_dev1 = :voltage_dev1, live_current_dev1 = :current_dev1, live_power_dev1 = :power_dev1, live_voltage_dev2 = :voltage_dev2, live_current_dev2 = :current_dev2, live_power_dev2 = :power_dev2, main_status = :main_stats, dev1_status = :dev1_stats, dev2_status = :dev2_stats ',
        'ExpressionAttributeValues': {
            ':current_main': {'N': str(current_main)},
            ':voltage_main': {'N':str(voltage_main)},
            ':power_main': {'N': str(power_main)},
            ':current_dev1': {'N': str(current_dev1)},
            ':voltage_dev1': {'N':str(voltage_dev1)},
            ':power_dev1': {'N': str(power_dev1)},
            ':current_dev2': {'N': str(current_dev2)},
            ':voltage_dev2': {'N':str(voltage_dev2)},
            ':power_dev2': {'N': str(power_dev2)},
            ':main_stats': {"N": str(main_stats)},
            ':dev1_stats': {"N": str(dev1_stats)},
            ':dev2_stats': {"N": str(dev2_stats)}
        }
    }
    
    # Call the update_item method of the DynamoDBClient object
    response = dynamodb.update_item(**update_item_request)
    
    return response
