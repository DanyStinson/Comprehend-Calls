import json
import boto3

def lambda_handler(event, context):
    '''
    triggers a step function from the S3 landing event,
    passing along the S3 file info
    '''

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    input= {
            'bucket_name': bucket_name,
            'file_key': file_key
        }

    stepFunction = boto3.client('stepfunctions')

    response = stepFunction.start_execution(
        stateMachineArn='arn:aws:states:eu-west-1:ACCOUNTNUMBER:stateMachine:STATEMACHINENAME',
        input = json.dumps(input, indent=4)
    )


    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('File triggered a new process!')
    }
