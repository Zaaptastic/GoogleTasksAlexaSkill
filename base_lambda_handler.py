import os
import datetime as dt
from google_tasks_gateway import GoogleTasksGateway
from pytz import timezone

default_timezone = timezone('US/Eastern')
tasklist_id = os.environ['TASKLIST_ID']
tasks_gateway = GoogleTasksGateway()

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
    results = tasks_gateway.add_task_to_list(tasklist_id, item_to_add)
    print(results)

    message = build_PlainSpeech(prompt_text + " I've added " + item_to_add + " to your " + list_name + " List")
    return build_response(message)

def handle_get_items_intent(list_name):
    results = tasks_gateway.get_tasks_from_list(tasklist_id)
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
