import json
import boto3
import os

client = boto3.client('dynamodb')

def lambda_handler(event, context):

    '''
    Retrieve transcribe results uri sent to Comprehend Text Lambda
    '''

    comprehendResults = event['comprehendResults_ddb']
    print(comprehendResults)

    response = client.put_item(
        TableName= os.environ["DynamoTableName"],
        Item=comprehendResults
    )

    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Insights loaded into Dynamo!')
    }
