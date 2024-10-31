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

    def check_tag_information(self, table_name) -> tuple:
        db_path = os.path.join(self.folder_path, self.database_name)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                            SELECT count(*)
                            FROM {table_name};
                            """,
                (),
            )
            number_rows = cursor.fetchone()
            conn.close()
            return number_rows
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Tag information not inserted.")
            return False

    def run_sql_script(self, script_name) -> bool:  # ,database_name):
        db_path = os.path.join(self.folder_path, self.database_name)
        script_path = os.path.join(self.folder_path, script_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            with open(script_path, "r") as sql_file:
                cursor.executescript(sql_file.read())
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print("Error: ", e)
            print(f"The script {script_name} did not worked.")
            return False

    def database_creation(self) -> bool:
        db_status = self.check_database()

        if db_status == False:
            db_status = self.run_sql_script("database_schema.sql")

        tags = self.check_tag_information("tags")
        tag_categories = self.check_tag_information("tag_categories")
        tag_status = False

        if 0 in tags or 0 in tag_categories:
            db_status = self.run_sql_script("add_tag_information.sql")

        final_status = True if db_status or tag_status else False

        return final_status
