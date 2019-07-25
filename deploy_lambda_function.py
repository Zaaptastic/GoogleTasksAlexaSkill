import os

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("Beginning Lambda Deployment for 'GoogleTasksAlexaSkill'")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

test_output = os.system("python3 lambda_tests.py")
if 0 is not test_output:
	quit()
print("Tests passed! Bundling function code into ZIP archive")

zip_output = os.system("cd package && zip -r9 ../google_tasks_alexa_skill.zip . && cd ../ && zip -g google_tasks_alexa_skill.zip *lambda_handler.py")
if 0 is not zip_output:
	quit()
print("Created deployable ZIP archive, beginning Lambda Deployment")

upload_output = os.system("aws lambda update-function-code --function-name ToDoSync --zip-file fileb://google_tasks_alexa_skill.zip")
if 0 is not upload_output:
	quit()
print("Successfully deployed ToDoSync Lambda Function! Lambda UI may not immediately update.")

upload_output = os.system("aws lambda update-function-code --function-name ShoppingSync --zip-file fileb://google_tasks_alexa_skill.zip")
if 0 is not upload_output:
	quit()
print("Successfully deployed ShoppingSync Lambda Function! Lambda UI may not immediately update.")

clean_up_output = os.system("rm google_tasks_alexa_skill.zip")
if 0 is not clean_up_output:
	print("Error deleting artifacts! Please manually remove ZIP archive.")
print("Cleaned up artifacts, deployment completed and successful!")