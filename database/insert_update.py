import sqlite3

from database.select_db import SelectDB
from utils.var_global import VarGlobal

from datetime import date
import re
import os


class InsertUpdate:
    def __init__(self, database_name):
        self.database_name = database_name
        self.folder_path = VarGlobal.DATA_BASE_PATH
        # self.folder_path = os.path.basename(os.getcwd())

    def update_insert_readme(self, data_dict, platform, description=None):
        db_path = os.path.join(self.folder_path, self.database_name)

        platform = "openvino" if "openvino" in str(platform).lower() else platform
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    INSERT INTO {VarGlobal.TABLE_METADATA_PREMAP} (id_name, name, link, description, platform, update_date)
                    VALUES (?,?,?,?,?,?)
                    ON CONFLICT(id_name) DO UPDATE SET 
                        update_date = excluded.update_date
                """,
                (
                    re.sub(r"[^a-z0-9\s]", "", data_dict["Name"].lower()),
                    data_dict["Name"],
                    data_dict["Link"],
                    description,
                    platform,
                    str(date.today()),
                ),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_insert_readme)")

    def update_raw_readme(self, registry):
        db_path = os.path.join(self.folder_path, self.database_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    UPDATE {"metadata_premap"}
                    SET description = ?
                    WHERE id_name = ?
                    """,
                (
                    registry[3],
                    registry[0],
                ),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_raw_readme)")

    def update_insert_smartsheet(self, data_dict: dict, table_name: str) -> None:
        db_path = os.path.join(self.folder_path, self.database_name)
        keys = ", ".join(data_dict.keys())

        # Fix it to be agnostic to the colums

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""INSERT OR REPLACE INTO {table_name} (prim, demo_type, demo_description, demo_link, demo_team, usage_requirements, tech, start_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                (
                    # data_dict["Primary"].lower().replace(" ", ""),
                    re.sub(r"[^a-z0-9 ]", "", data_dict["Primary"].lower()),
                    data_dict["Demo Type"],
                    data_dict["Demo Description"],
                    data_dict["Link to Demo"],
                    data_dict["Demo Team"],
                    data_dict["Usage Requirements"],
                    None,
                    date.today(),
                    data_dict["Status"],
                ),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_insert_smartsheet)")

    # def update_premap_smartsheet(self):
    def insert_ignore_smartsh(self):

        try:
            db_path = os.path.join(self.folder_path, self.database_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT OR IGNORE INTO metadata_premap (id_name, name, link, description, platform, summary, update_date)
                SELECT 
                    replace(prim, " ", "") as id, 
                    prim, 
                    demo_link, 
                    demo_description, 
                    CASE 
                        WHEN demo_link like "%inteleventexpress.%" THEN "inteleventexpress"
                        WHEN demo_link like "%sharepoint.%" THEN "sharepoint"
                        WHEN demo_link like "%digitallibrary.%" THEN "digitallibrary"
                        WHEN demo_link like "%onlinexperiences.%" THEN "onlinexperiences"
                        WHEN demo_link like "%intel.%" THEN "intel"
                        WHEN demo_link like "%youtube.%" THEN "youtube"
                        ELSE "other"
                    END as 'platform',
                    NULL, 
                    start_date
                FROM ai_demo_dashboard
                """
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_premap_smartsheet)")

    def update_one_where(
        self,
        table_name: str,
        key_name: str,
        field_name: str,
        key_value: str,
        value_set: str,
    ) -> None:
        db_path = os.path.join(self.folder_path, self.database_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    UPDATE  
                        {table_name} 
                    SET 
                        {field_name} = ? 
                    WHERE
                        {key_name} = ?
                        ;
                """,
                (value_set, key_value),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_one_where)")

    def update_map_with_premap(self, destination_table, origin_table) -> None:
        db_path = os.path.join(self.folder_path, self.database_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""INSERT OR REPLACE INTO {destination_table} (id_name, title, path, imageUrl, createDate,  modifiedDate, link)	
                    SELECT id_name, name, link, NULL, update_date, CURRENT_DATE, link
                    FROM {origin_table}
                    WHERE summary is not NULL
                    """
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_premap_with_map)")

    def update_map_with_table(
        self, destination_table: str, origin_table: str, column_names: list
    ) -> None:
        db_path = os.path.join(self.folder_path, self.database_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(  # the query has the values to be inserted necessary, the select could be dyanamic
                f"""INSERT OR REPLACE INTO {destination_table} (id_name, title, path, imageUrl, createDate,  modifiedDate, link)	
                    SELECT {(','.join( "'"+str(x)+"'" for x in column_names))}""",  # this need to be replace to take any type of names
                f"""FROM {origin_table}
                    WHERE summary is not NULL
                    """,
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_map_with_table) failed to update")

    def insert_tags_map(self, foreign_key: str, category: str, tag: list) -> None:
        db_path = os.path.join(self.folder_path, self.database_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO metadata_tags_map ( metadata_id, tag_id )
                SELECT '{foreign_key}', t.tag_id
                FROM tags as t
                LEFT JOIN tag_categories as tc
                on	t.category_id = tc.category_id
                WHERE lower (tc.category_name) = lower('{category}')
                AND t.tag_name in({(','.join( "'"+str(x)+"'" for x in tag))})
                    """
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error: ", e.args)
            print("Data not inserted (def insert_tags_map)")

    def insert_dict_json(self, id_name: str, sql_result: dict) -> bool:
        try:
            db_path = os.path.join(self.folder_path, self.database_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    INSERT OR REPLACE INTO json_formatted_data (id_name, dict_data)
                    VALUES(?,?);
                """,
                (id_name, str(sql_result)),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print("Error: ", e.args)
            print("Data not inserted (def insert_tags_map)")
            return False

    def update_json_formatted_data(self) -> bool:
        try:
            db_path = os.path.join(self.folder_path, self.database_name)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    UPDATE json_formatted_data SET status = 'completed' WHERE status = 'latest';
                """,
                (),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print("Error: ", e.args)
            print("Data not inserted (def update_json_formatted_data)")
            return False
