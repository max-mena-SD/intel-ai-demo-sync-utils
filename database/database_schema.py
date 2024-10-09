import sqlite3
import os


class StartDatabase:
    def __init__(self, database_name):
        self.database_name = database_name

    def check_database(self):
        folder_path = "database"
        db_path = os.path.join(folder_path, self.database_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if len(tables) == 0:
                raise sqlite3.Error("No tables found.")
            conn.close()
            print("Database exists.")
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Database does not exist. Creating database...")
            StartDatabase.create_database(db_path)

    def create_database(database_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        with open("database/database_schema.sql", "r") as sql_file:
            cursor.executescript(sql_file.read())

        conn.commit()
        conn.close()
        print("Database and table created successfully.")
