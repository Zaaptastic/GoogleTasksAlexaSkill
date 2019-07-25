# Overdue

The goal of this Project is to bridge a feature gap in adding and managing items from a Google Tasks list via an Alexa Skill

Much of the initial code was copied over from [this Project](https://github.com/Zaaptastic/Overdue), which was used to notify users on Tasks overdue for completion on a regular cadence. 

## Making Code Changes

The following steps must be followed in order to create a deployable .zip file for GoogleTasksAlexaSkill.

### Install Dependencies

The following dependencies should be installed with the following command:

```
pip3 install pytz google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Generate Authentication Token

This requires having a Google API Project to enable API access to the Tasks API.

First, create a file named `credentials.json` in your package root directory and add your Google API credentials to it. These credentials can be created and managed in the [Google API Console](https://console.developers.google.com/apis/credentials).

Run the following command and copy/paste the URL provided. 

```
python3 generate_token.py
```

After properly authenticating, you should notice a file named `token.pickle` appear in the package root directory. Upload this token to a dedicated, private bucket on S3.

### Running Deployment Script
Assuming you have your AWS CLI correctly configured, you can take advantage of a handy script provided in the root package directory to easily test, build, and deploy your Lambda Function. Simply run the command:

```
python3 deploy_lambda_function.py
```

If this works for you, then great! You don't need to follow any of the other steps in this section for deploying your code changes.

### Running Unit Tests

If you are trying to solely run the unit tests and not trigger a deployment, you can run the following command: 

```
python3 lambda_tests.py
```

### Generate .zip file and Uploading Manually

The following command creates the .zip file and adds the package dependencies to it

```
cd package
zip -r9 ../google_tasks_alexa_skill.zip .
```

Next, run the following command to add the handler function code and your token to the .zip archive.

```
cd ../
zip -g google_tasks_alexa_skill.zip *lambda_handler.py
```

Done! Now you should have a complete `google_tasks_alexa_skill.zip` file that you can upload to your Lambda Function.

## Configuring Lambda

After uploading the .zip archive to a created Lambda Function, there are only a few additional steps needed to get your own personal Function up and running.

1. Add the following Environment Variables to your Lambda Function:
    1. Key: `TASKLIST_ID`, Value: `<ID of TaskList you wish to attach Function to>`
    1. Key: `S3_BUCKET_NAME`, Value: `<Name of S3 Bucket containing authentication token>`
    1. Key: `S3_FILE_NAME`, Value: `<Name of authentication token file>`
1. Add the following IAM Permissions (via a new or existing IAM Role) to your Lambda Function: `AWSLambdaBasicExecutionRole`, and `AmazonS3ReadOnlyAccess`
1. Set up an Alexa Skill and point to to your Lambda ARN as a Trigger
