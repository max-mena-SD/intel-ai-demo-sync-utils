from datetime import date
import sqlite3

import os


class InsertUpdate:
    def __init__(self, database_name):
        self.database_name = database_name
        self.folder_path = "database"
        # self.folder_path = os.path.basename(os.getcwd())

    def update_insert_readme(self, data_dict, platform):
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
                    data_dict["Name"].replace("-", "").lower(),
                    data_dict["Name"],
                    data_dict["Link"],
                    None,
                    platform,
                    None,
                    str(date.today()),
                ),
            )
            conn.commit()
            conn.close()
            print("Data inserted successfully")
        except sqlite3.Error as e:
            print("Error: ", e)
            print("Data not inserted (def update_insert_readme)")
