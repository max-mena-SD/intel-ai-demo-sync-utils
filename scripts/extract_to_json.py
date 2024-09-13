import json
import requests
from bs4 import BeautifulSoup as bs


class ExtractToJSON:

    def __init__(self, output_path):
        self.url = "https://github.com/openvinotoolkit/openvino_notebooks/tree/latest/notebooks"
        self.output_path = output_path

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
