import requests
import database

from utils import var_global as v


class ReadmeExtraction:
    def __init__(self, url):
        self.url = url

    def one_readme_file(self, notebook_name):
        url = f"{self.url}/{notebook_name}/README.md"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error downloading {notebook_name}: {e}"
        except IOError as e:
            return f"Error saving file {self.path_name}: {e}"

    def get_readme(self):  # instead of looking for the json will receive a sql
        reg_mod = []
        registry = database.SelectDB(v.VarGlobal.DATABASE_NAME).select_one_where(
            "metadata_premap", "description is NULL"
        )
        if registry:
            raw_readme = self.one_readme_file(registry[1])
            reg_mod = list(registry)
            reg_mod[3] = raw_readme
            return reg_mod
        return None

    def save_readme(self, registry_list=None):

        if registry_list:
            insert_reg = registry_list
            database.InsertUpdate(v.VarGlobal.DATABASE_NAME).update_raw_readme(
                insert_reg
            )
        else:
            print("No registry to insert")

    def get_all_readme(self):
        empty_description = self.get_readme()
        while empty_description:
            self.save_readme(empty_description)
            try:
                empty_description = self.get_readme()
            except Exception as e:
                print(f"Error (all readme files processed): {e}")
                break
