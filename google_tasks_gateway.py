import boto3
import os
import pickle
from pytz import timezone
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleTasksGateway:
    tasks_service_client = None

    def __init__(self):
        s3 = boto3.resource('s3')
        # Grab credentials from S3 drop point and construct service client.
        creds = None
        if 'TEST_DOMAIN' not in os.environ:
            with BytesIO() as data:
                s3.Bucket(os.environ['S3_BUCKET_NAME']).download_fileobj(os.environ['S3_FILE_NAME'], data)
                data.seek(0)    # move back to the beginning after writing
                creds = pickle.load(data)
            tasks_service_client = build('tasks', 'v1', credentials=creds)
            self.tasks_service_client = tasks_service_client

    def get_tasks_from_list(self, tasklist_id):
        return self.tasks_service_client.tasks().list(tasklist=tasklist_id, showCompleted=False).execute()

    def add_task_to_list(self, tasklist_id, item_to_add):
        return self.tasks_service_client.tasks().insert(tasklist=tasklist_id, body={"title": item_to_add.capitalize()}).execute()
