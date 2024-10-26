from utils.var_global import VarGlobal

import sqlite3

import os


class SelectDB:
    def __init__(self, db):
        self.db = db
        self.folder_path = VarGlobal.DATA_BASE_PATH  # "database"
        # self.folder_path = os.path.basename(os.getcwd())

    def select_all(self, table_name) -> list:
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

    def select_one_where(self, table_name, where) -> tuple:
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
        self, first_table_name, second_table_name, first_key, second_key, where
    ) -> tuple:
        db_path = os.path.join(self.folder_path, self.db)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""SELECT a.*
                FROM {first_table_name} as a
                LEFT JOIN {second_table_name} as b
                ON a.{first_key} = b.{second_key}
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

    def select_tags_demo(self, id_name: str):
        """
        Process will eliminate anything related to the id_name in metadata_tags_map before inserting any new tags.
        Returns the information needed to build a JSON object for a specific metadata entry based on its id_name.
        """
        db_path = os.path.join(self.folder_path, self.db)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                SELECT tc.category_name, t.tag_name
                FROM metadata_tags_map mtm
                JOIN tags t ON mtm.tag_id = t.tag_id
                JOIN tag_categories tc ON t.category_id = tc.category_id
                WHERE mtm.metadata_id = ?
            """,
                (id_name,),
            )
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Query not executed (def select_tags_demo)")
            return None
