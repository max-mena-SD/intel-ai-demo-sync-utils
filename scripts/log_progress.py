from datetime import datetime


class LogProcess:
    def __init__(self, log_file):
        self.log_file = log_file
        self.name_file = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} : {message}"
        try:
            with open(self.log_file + self.name_file, "a") as f:
                f.write(formatted_message + "\n")
        except IOError as e:
            print(f"Error writing to log file: {e}")

    def read(self):
        try:
            with open(self.log_file + self.name_file, "r") as f:
                return f.read()
        except IOError as e:
            print(f"Error reading log file: {e}")
            return ""
