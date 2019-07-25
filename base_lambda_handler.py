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

def handle_add_item_intent(item_to_add, list_name, prompt_text):
    results = tasks_service_client.tasks().insert(tasklist=tasklist_id, body={"title": item_to_add.capitalize()}).execute()
    print(results)

    message = build_PlainSpeech(prompt_text + " I've added " + item_to_add + " to your " + list_name + " List")
    return build_response(message)

def handle_get_items_intent(list_name):
    results = tasks_service_client.tasks().list(tasklist=tasklist_id, showCompleted=False).execute()
    print(results)

    items = results.get('items', [])

    if not items:
        return build_response(build_PlainSpeech("Your " + list_name + " list is empty"))
    elif len(items) is 1:
        return build_response(build_PlainSpeech("Your " + list_name + " list contains one item: " + items[0]['title']))
    else:
        list_as_string = ""
        last_item = items.pop()

        for item in items:
            list_as_string = list_as_string + item['title'] +", "

        list_as_string = list_as_string + "and " + last_item['title']
        return build_response(build_PlainSpeech("Your " + list_name + " list contains " + str(len(items) + 1) + " items: " + list_as_string)) 

def base_handle(event, context, list_name, prompt_text):
    print("Beginning Lambda Handler Execution for " + list_name + " List Synchronization.")
    print(event['request']['type'])
    if event['request']['type'] == "LaunchRequest":
        return handle_get_items_intent(list_name)
    if event['request']['type'] == "IntentRequest":
        item_to_add = event['request']['intent']['slots']['item_to_add']['value']
        return handle_add_item_intent(item_to_add, list_name, prompt_text)

def handle_shopping_sync(event, context):
    return base_handle(event, context, "Shopping", "Good job, you did it!")

def handle_to_do_sync(event, context):
    return base_handle(event, context, "To Do", "Ok, done.")
