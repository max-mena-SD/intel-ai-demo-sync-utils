import unittest
import os
import sys

# from datetime import datetime

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.log_progress import LogProcess


class TestLogProcess(unittest.TestCase):
    def setUp(self):
        # Create a temporary log directory
        self.log_dir = "temp_logs/"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = self.log_dir + "test_log_"
        self.logger = LogProcess(self.log_file)

    def tearDown(self):
        # Clean up the temporary log directory
        for file in os.listdir(self.log_dir):
            os.remove(os.path.join(self.log_dir, file))
        os.rmdir(self.log_dir)

    def test_log_creation(self):
        message = "This is a test log message."
        self.logger.log(message)
        log_file_path = self.log_file + self.logger.name_file
        self.assertTrue(os.path.exists(log_file_path))

    def test_log_content(self):
        message = "This is a test log message."
        self.logger.log(message)
        log_file_path = self.log_file + self.logger.name_file
        with open(log_file_path, "r") as f:
            content = f.read()
        self.assertIn(message, content)

    def test_read_log(self):
        message = "This is a test log message."
        self.logger.log(message)
        content = self.logger.read()
        self.assertIn(message, content)


if __name__ == "__main__":
    unittest.main()
