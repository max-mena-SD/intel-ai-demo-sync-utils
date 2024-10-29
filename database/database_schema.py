import sqlite3

import os


class StartDatabase:
    def __init__(self, database_name):
        self.database_name = database_name
        self.folder_path = "database"
        # self.folder_path = os.path.basename(os.getcwd())

    def check_database(self) -> bool:
        db_path = os.path.join(self.folder_path, self.database_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if len(tables) == 0:
                raise sqlite3.Error("No tables found.")
            conn.close()
            print("Database exists.")
            return True
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Database does not exist.")
            return False

    def create_database(self) -> bool:  # ,database_name):
        db_path = os.path.join(self.folder_path, self.database_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            with open("database/database_schema.sql", "r") as sql_file:
                cursor.executescript(sql_file.read())
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Database is not created.")
            return False

    def add_tag_information(self) -> bool:  # ,database_name):
        db_path = os.path.join(self.folder_path, self.database_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            with open("database/add_tag_information.sql", "r") as sql_file:
                cursor.executescript(sql_file.read())
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Tags were not added.")
            return False

    def database_creation(self) -> bool:
        db_status = False
        tag_status = False

        db_status = self.check_database()

        if db_status == False:
            db_status = self.create_database()
            if db_status == True:
                tag_status = self.add_tag_information()

        final_status = db_status == tag_status

        return final_status
