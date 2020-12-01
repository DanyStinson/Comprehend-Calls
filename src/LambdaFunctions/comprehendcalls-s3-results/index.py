import json
import boto3
import os

s3 = boto3.resource('s3')
bucket = s3.Bucket(os.environ["OutputBucket"])

def lambda_handler(event, context):

    comprehendResults = event['comprehendResults_s3']
    print(json.dumps(comprehendResults, ensure_ascii=False))
    response_s3 = bucket.put_object(
            Body = json.dumps(comprehendResults, ensure_ascii=False),
            Key = "transcriptions-insights/"+event["transcriptionid"].split(".")[0]+".json"
        )

    print(response_s3)

    return {
        'statusCode': 200,
        'body': json.dumps('Insights loaded into S3!')
    }
