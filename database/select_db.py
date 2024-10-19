from utils.var_global import VarGlobal

import sqlite3

import os


class SelectDB:
    def __init__(self, db):
        self.db = db
        self.folder_path = VarGlobal.DATA_BASE_PATH  # "database"
        # self.folder_path = os.path.basename(os.getcwd())

    def select_all(self, table_name):
        db_path = os.path.join(self.folder_path, self.db)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def select_all)")
            return None

    def select_one_where(self, table_name, where):
        db_path = os.path.join(self.folder_path, self.db)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE {where}")
            rows = cursor.fetchone()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def select_where)")
            return None

    def select_one_join_where(
        self, first_table_name, second_table_name, join_key, where
    ):
        db_path = os.path.join(self.folder_path, self.db)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""SELECT a.*
                FROM {first_table_name} as a
                LEFT JOIN {second_table_name} as b
                ON a.{join_key} = b.{join_key}
                WHERE {where}
                """
            )
            rows = cursor.fetchone()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def select_one_join_where)")
            return None
