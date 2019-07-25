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

sns = boto3.client('sns')
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

def publish_message_to_sns(task_title):
	message = "You have one overdue task: " + task_title
	
	response = sns.publish(
		TopicArn=os.environ['SNS_ARN'], 
		Message=message,
		Subject=task_title)
	
	return response
	
def is_time_overdue(time_string):
	# We run into a limitation with the Tasks API not providing information more precise than day.
	# Therefore, these alerts could be inaccurate if this function is called on the day of the
	# task is due, but before the time at which it is due (False Positive).
	due_time = default_timezone.localize(dt.datetime.strptime(time_string, '%Y-%m-%d'))
	overdue_time = dt.datetime.now(default_timezone)

	print("\t\tProcessing due time: " + str(due_time), ". Will consider overdue if after: " + str(overdue_time))
	if overdue_time >= due_time:
		return True
	return False

def handle_overdue_tasks(event, context):
	# Call the Tasks API
	results = tasks_service_client.tasklists().list(maxResults=10).execute()
	items = results.get('items', [])

	if not items:
		print('No task lists found.')
	else:
		print('Task lists:')
		for item in items:
			print(u'{0} ({1})'.format(item['title'], item['id']))
			
			results = tasks_service_client.tasks().list(tasklist=item['id']).execute()
			tasks_list = results.get('items', [])
			for task_item in tasks_list:
				print("\tProcessing task: " + task_item['title'])
				if 'due' in task_item.keys():
					if is_time_overdue(str(task_item['due']).split('T')[0]):
						print("\t\tTask is overdue, sending SNS reminder")
						publish_message_to_sns(task_item['title'])
			
	return "Done!"