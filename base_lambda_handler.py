import boto3
import os
import pickle
import datetime as dt
from pytz import timezone
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

s3 = boto3.resource('s3')
default_timezone = timezone('US/Eastern')

# Grab credentials from S3 drop point and construct service client.
creds = None
if 'TEST_DOMAIN' not in os.environ:
    with BytesIO() as data:
        s3.Bucket(os.environ['S3_BUCKET_NAME']).download_fileobj(os.environ['S3_FILE_NAME'], data)
        data.seek(0)    # move back to the beginning after writing
        creds = pickle.load(data)
    tasks_service_client = build('tasks', 'v1', credentials=creds)
    tasklist_id = os.environ['TASKLIST_ID']

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = {'outputSpeech':message}
    return response
    
def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def base_handle(event, context, list_name, prompt_text):
    print("Beginning Lambda Handler Execution for " + list_name + " List Synchronization.")
    print(event['request']['type'])
    if event['request']['type'] == "LaunchRequest":
        message = build_PlainSpeech("Welcome to " + list_name + " Sync skill")
        return build_response(message)
    if event['request']['type'] == "IntentRequest":
        item_to_add = event['request']['intent']['slots']['item_to_add']['value']

        results = tasks_service_client.tasks().insert(tasklist=tasklist_id, body={"title": item_to_add.capitalize()}).execute()
        print(results)

        message = build_PlainSpeech(prompt_text + " I've added " + item_to_add + " to your " + list_name + " List")
        return build_response(message)


def handle_shopping_sync(event, context):
    return base_handle(event, context, "Shopping", "Good job, you did it!")

def handle_to_do_sync(event, context):
    return base_handle(event, context, "To Do", "Ok, done.")
