import json
import boto3

iot_client = boto3.client('iot-data')

def lambda_handler(event, context):
    # TODO implement
    
    print(event)
    
    bodcontent = event["body"]
    
    py_obj = json.loads(bodcontent)
    
    val = py_obj["value"]
    stats = py_obj["stats"]
    
    string = "mainon"
    
    if val == 1:
        if stats:
            string = "mainon"
        else:
            string = "mainoff"
    
    elif val == 2:
        if stats:
            string = "dev1on"
        else:
            string = "dev1off"
    
    elif val == 3:
        if stats:
            string = "dev2on"
        else:
            string = "dev2off"
    
    message = {"message":string}
    
    message_json = json.dumps(message)
    
    iot_client.publish(
        topic='esp32/sub',
        payload=message_json
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
