from utils import var_global as v
import database

import pandas as pd

import os


class SmartsheetExtractor:
    def __init__(self, token: str):
        self.token = token

    # If the token is working this function won't be necessary
    def __init__(self):
        self.path = os.path.join(v.VarGlobal.DATA_PATH, v.VarGlobal.SMARTSHEET_AI_DEMO)

    def extract_data_excel(self):
        # Extract data from Smartsheet Excel file
        try:
            df = pd.read_excel(self.path)
            content_dict = df.to_dict(orient="records")
            return content_dict
        except Exception as e:
            print(f"Error (extract_data_excel): {e}")
        return None

    def save_data_to_table(self, data_dict, table_name):
        # Save data in the database
        db = database.InsertUpdate(v.VarGlobal.DATABASE_NAME)
        db.update_insert_smartsheet(data_dict, table_name)

    def save_all_to_table(self):
        dict_data = self.extract_data_excel()
        for data in dict_data:
            self.save_data_to_table(data, v.VarGlobal.TABLE_AI_DEMO_DASH)
            # return 0
