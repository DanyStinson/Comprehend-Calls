import json
import boto3
import time

client = boto3.client('transcribe')


def lambda_handler(event, context):

    '''
    Retrieve bucket and key sent to Transcribe Audio Lambda
    '''

    bucket = event['bucket_name']
    key = event['file_key']


    start_transcription_response = client.start_transcription_job(
        TranscriptionJobName='Transcription-'+key.split("/")[1],
        LanguageCode='es-ES',
        MediaFormat='mp3',
        Media={
            'MediaFileUri': "s3://"+bucket+"/"+key
        },
        OutputBucketName='comprehendcalls-output',

    )

    print(start_transcription_response)

    while True:
        status = client.get_transcription_job(TranscriptionJobName="Transcription-"+key.split("/")[1])
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            print("Complete")
            break
        print("Not ready yet...")
        time.sleep(10)
    print(f"transcript URL is {status['TranscriptionJob']['Transcript']['TranscriptFileUri']}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from the Transcribe Audio Lambda!'),
        'transcribeUri': json.dumps(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    }
