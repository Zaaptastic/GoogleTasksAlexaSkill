import unittest
from unittest.mock import patch, Mock
import os
os.environ['S3_FILE_NAME'] = "test_file_name"
os.environ['S3_BUCKET_NAME'] = "test_bucket_name"
os.environ['SNS_ARN'] = "test_sns_arn"
os.environ['TEST_DOMAIN'] = "True"
os.environ['TASKLIST_ID'] = "test_tasklist_id"

import base_lambda_handler

class TestStringMethods(unittest.TestCase):
	# Declare reusable mock values
	tasks_list_with_no_items = {"items" : [ ]}
	tasks_list_with_one_item = {"items" : [ {"title":"Item1"} ]}
	tasks_list_with_multiple_items = {"items" : [ {"title":"Item1"}, {"title":"Item2"}, {"title":"Item3"} ]}

	# Test Get_Tasks Directly
	@patch("base_lambda_handler.tasks_gateway.get_tasks_from_list", unittest.mock.MagicMock(return_value=tasks_list_with_no_items))
	def test_get_items_on_list_with_no_items(self):
		result = base_lambda_handler.handle_get_items_intent("TEST")
		self.assertTrue(result["response"]["outputSpeech"]["text"] == "Your TEST list is empty")

	@patch("base_lambda_handler.tasks_gateway.get_tasks_from_list", unittest.mock.MagicMock(return_value=tasks_list_with_one_item))
	def test_get_items_on_list_with_one_item(self):
		result = base_lambda_handler.handle_get_items_intent("TEST")
		self.assertTrue(result["response"]["outputSpeech"]["text"] == "Your TEST list contains one item: Item1")

	@patch("base_lambda_handler.tasks_gateway.get_tasks_from_list", unittest.mock.MagicMock(return_value=tasks_list_with_multiple_items))
	def test_get_items_on_list_with_multiple_items(self):
		result = base_lambda_handler.handle_get_items_intent("TEST")
		self.assertTrue(result["response"]["outputSpeech"]["text"] == "Your TEST list contains 3 items: Item1, Item2, and Item3")

	# Test Add_Task Directly
	@patch("base_lambda_handler.tasks_gateway.add_task_to_list",  unittest.mock.MagicMock(return_value=""))
	def test_add_items(self):
		result = base_lambda_handler.handle_add_item_intent("NewItem", "TEST", "TEST TEXT.")
		self.assertTrue(result["response"]["outputSpeech"]["text"] == "TEST TEXT. I've added NewItem to your TEST List")

if __name__ == '__main__':
	unittest.main()