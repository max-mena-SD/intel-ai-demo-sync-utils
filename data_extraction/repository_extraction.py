import logging
from time import sleep
import json
import requests
from bs4 import BeautifulSoup as bs

import database
from utils.var_global import VarGlobal


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
        max_attempts = 5
        backoff_factor = 2  # Aumenta el tiempo de espera exponencialmente

        for attempt in range(max_attempts):
            try:
                table = self.extract_notebooks()

                if table is None:
                    raise ValueError("No se pudo extraer la tabla")

                data_dict = self.parse_notebooks(table)

                if not data_dict:
                    raise ValueError("No hay datos para guardar")

                for data in data_dict.values():
                    try:
                        self.save_into_database(
                            data, VarGlobal.DATABASE_NAME, VarGlobal.OPENVINO_REPOSITORY
                        )
                    except Exception as db_error:
                        logging.error(f"Error guardando en DB: {db_error}")

                return True  # Éxito

            except Exception as e:
                wait_time = (backoff_factor**attempt) * 10
                logging.warning(f"Intento {attempt + 1}/{max_attempts} fallido: {e}")
                sleep(wait_time)

        logging.error(
            "Extracción y guardado de notebooks fallido después de máximos intentos"
        )
        return False
