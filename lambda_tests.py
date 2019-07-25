import unittest
import os
os.environ['S3_FILE_NAME'] = "test_file_name"
os.environ['S3_BUCKET_NAME'] = "test_bucket_name"
os.environ['SNS_ARN'] = "test_sns_arn"
os.environ['TEST_DOMAIN'] = "True"

class TestStringMethods(unittest.TestCase):

	def test_empty_test(self):
		self.assertTrue(True)

if __name__ == '__main__':
	unittest.main()