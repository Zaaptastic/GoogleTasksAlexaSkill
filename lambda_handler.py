import overdue_tasks_lambda_handler
import to_do_sync_lambda_handler
import shopping_sync_lambda_handler
	
def overdue_tasks_handler(event, context):
	print("Beginning Lambda Handler Execution for Overdue Task Notifications.")
	return overdue_tasks_lambda_handler.handle_overdue_tasks(event, context)

def to_do_sync_handler(event, context):
	print("Beginning Lambda Handler Execution for To-Do List Synchronization.")
	return to_do_sync_lambda_handler.handle_to_do_sync(event, context)

def shopping_sync_handler(event, context):
	print("Beginning Lambda Handler Execution for Shopping List Synchronization.")
	return shopping_sync_lambda_handler.handle_shopping_sync(event, context)