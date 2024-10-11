import sqlite3

from datetime import date
import re
import os


class InsertUpdate:
    def __init__(self, database_name):
        self.database_name = database_name
        self.folder_path = "database"
        # self.folder_path = os.path.basename(os.getcwd())

    def update_insert_readme(self, data_dict, platform, description=None):
        db_path = os.path.join(self.folder_path, self.database_name)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    INSERT INTO {"metadata_premap"} (id_name, name, link, description, platform, summary, update_date)
                    VALUES (?,?,?,?,?,?,?)
                    ON CONFLICT(id_name) DO UPDATE SET 
                        name = excluded.name,
                        link = excluded.link,
                        description = excluded.description,
                        platform = excluded.platform,
                        summary = excluded.summary,
                        update_date = excluded.update_date
                """,
                (
                    re.sub(r"[^a-z0-9\s]", "", data_dict["Name"].lower()),
                    data_dict["Name"],
                    data_dict["Link"],
                    description,
                    platform,
                    None,
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
