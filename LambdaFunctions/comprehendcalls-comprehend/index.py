import json
import boto3
import urllib3

s3 = boto3.resource('s3')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):

    '''
    Retrieve transcribe results uri sent to Comprehend Text Lambda
    '''
    uri = event['transcribeUri']
    print(uri)

    #Get bucket and key names

    bucket = uri.split('"')[1].split("/")[3]
    key = uri.split('"')[1].split("/")[4]+'/'+uri.split('"')[1].split("/")[5]

    print("Bucket: " + bucket + " , Key = " + key)

    #Get object
    obj = s3.Object(bucket, key)
    body = obj.get()['Body'].read()

    #Encode object
    encoding = 'utf-8'
    json_text = json.loads(body.decode(encoding))
    transcript = json_text['results']['transcripts'][0]['transcript']

    # Define response

    response_values_ddb = {}
    response_values_s3 = []
    response_values_ddb["TranscriptionId"] = {"S":key.split("/")[1].split(".json")[0]}

    # Get language
    language_response = comprehend.detect_dominant_language(
        Text=transcript
    )

    language=language_response["Languages"][0]["LanguageCode"]
    #print("Language: " + language)
    response_values_ddb["Language"] = {"S":language}

    # Get sentiment
    sentiment_response = comprehend.detect_sentiment(
        Text=transcript,
        LanguageCode=language_response["Languages"][0]["LanguageCode"]
    )
    sentiment = sentiment_response["Sentiment"]
    #print("Sentiment: " + sentiment)
    response_values_ddb["Sentiment"] = {"S":sentiment}


    # Get entities
    entities_response = comprehend.batch_detect_entities(
        TextList=[transcript],
        LanguageCode=language_response["Languages"][0]["LanguageCode"]
    )
    entities = entities_response["ResultList"][0]["Entities"]
    #print(entities)
    entity_list_ddb ={}
    entity_list_s3 =[]
    for entity in entities:
        entity_list_ddb[entity["Text"]]={"S":entity["Type"]}
        response_values_s3.append({
            "TranscriptionId":key.split("/")[1].split(".json")[0],
            "Language":language,
            "Sentiment":sentiment,
            "Entity_type":entity["Type"],
            "Entity_text":entity["Text"]
        })
    #print("Entities DDB: ")
    #print(entity_list_ddb)
    #print("Entities S3: ")
    #print(entity_list_s3)
    response_values_ddb["Entities"] = {"M":entity_list_ddb}

    #print(response_values_ddb)
    #print(response_values_s3)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'comprehendResults_ddb' : response_values_ddb,
        'comprehendResults_s3' : response_values_s3,
        'transcriptionid':key.split("/")[1].split(".json")[0]
    }
