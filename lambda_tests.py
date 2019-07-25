import unittest
import os
os.environ['S3_FILE_NAME'] = "test_file_name"
os.environ['S3_BUCKET_NAME'] = "test_bucket_name"
os.environ['SNS_ARN'] = "test_sns_arn"
os.environ['TEST_DOMAIN'] = "True"

import datetime as dt
import overdue_tasks_lambda_handler as class_under_test

not_overdue_time = str(dt.datetime.now() + dt.timedelta(days=1)).split(' ')[0]
overdue_time = str(dt.datetime.now() - dt.timedelta(days=1)).split(' ')[0]

class TestStringMethods(unittest.TestCase):

	def test_not_overdue(self):
		result = class_under_test.is_time_overdue(not_overdue_time)
		self.assertFalse(result)

	def test_overdue_by_1_day(self):
		result = class_under_test.is_time_overdue(overdue_time)
		self.assertTrue(result)

if __name__ == '__main__':
	unittest.main()