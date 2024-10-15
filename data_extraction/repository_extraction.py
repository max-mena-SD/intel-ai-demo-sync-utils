from datetime import time
import json
import requests
from bs4 import BeautifulSoup as bs

import database
import utils


class RepositoryExtraction:

    def __init__(self, table_name, url):
        self.url = url
        self.table_name = table_name

    def extract_notebooks(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad status codes
            page = bs(response.text, "html.parser")
            table = page.find("tbody")
            if table:
                return table.find_all("tr")
            else:
                print("The table list is empty.")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching notebooks: {e}")
            return []

    def parse_notebooks(self, rows):
        data_dict = {}
        for row in rows:
            a_tag = row.find("a")
            if a_tag and "title" in a_tag.attrs and "href" in a_tag.attrs:
                name = a_tag["title"]
                data_dict[str(name)] = {"Name": name, "Link": a_tag["href"]}
        return data_dict

    def load_to_json(self, data_dict):
        try:
            with open(self.output_path, "w", encoding="utf-8") as file:
                json.dump(data_dict, file, indent=4, ensure_ascii=False)
            print("Loaded to JSON completed")
        except IOError as e:
            print(f"Error saving JSON file: {e}")

    def save_into_database(self, data_dict, db_name, platform):
        try:
            # database function
            database.InsertUpdate(db_name).update_insert_readme(data_dict, platform)
        except Exception as e:
            print(f"Error saving to database from (repository_extraction): {e}")

    def extract_save_notebooks(self):
        attempts = 2
        table = None
        for _ in range(attempts):
            table = self.extract_notebooks()
            if table is not None:
                break
            else:
                time.sleep(5)
                print("Sleeping for 5 seconds")
        data_dict = self.parse_notebooks(table)
        db_name = utils.Config.DATABASE_NAME
        platform = utils.Config.OPENVINO_REPOSITORY  # "OpenVINO"

        for data in data_dict.values():
            self.save_into_database(data, db_name, platform)
