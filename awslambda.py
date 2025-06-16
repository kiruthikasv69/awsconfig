import boto3
import json
#Used to parse JSON-formatted strings (because AWS Config sends data in JSON format).

def lambda_handler(event, context):

    # Get the specific EC2 instance.
    ec2_client = boto3.client('ec2')
    
    # Assume compliant by default
    compliance_status = "COMPLIANT"  
    
    # Extract the configuration item from the invokingEvent  
    #This is the event payload passed by AWS Config when it triggers your Lambda function.

    config = json.loads(event['invokingEvent'])
    
    configuration_item = config["configurationItem"]
#Extracts the configuration item, which has metadata about the EC2 instance being evaluated (like instance ID, current settings).
    
    # Extract the instanceId
    instance_id = configuration_item['configuration']['instanceId']
    
    # Get complete Instance details
    instance = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    
    # Check if the specific EC2 instance has Cloud watch enabled.
    
    if not instance['Monitoring']['State'] == "enabled":
        compliance_status = "NON_COMPLIANT"

    evaluation = {
        'ComplianceResourceType': 'AWS::EC2::Instance',
        'ComplianceResourceId': instance_id,
        'ComplianceType': compliance_status,
        'Annotation': 'Detailed monitoring is not enabled.',
        'OrderingTimestamp': config['notificationCreationTime']
    }

#This creates a dictionary (evaluation) that reports:
#What resource was checked (EC2)

#Which instance (instance_id)

#Whether it’s compliant or not

#Message annotation

#When this check was triggered
    
    config_client = boto3.client('config')
#Creates a client to interact with AWS Config (to send back results of evaluation).
    
    response = config_client.put_evaluations(
        Evaluations=[evaluation],
        ResultToken=event['resultToken'] #It is a unique token provided by AWS Config during the evaluation trigger.

#It is required when reporting the result back to AWS Config using put_evaluations().
    )  
    
    return response
