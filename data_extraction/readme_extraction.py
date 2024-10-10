import requests


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

    def transform_readme(self, readme_text):
        # it takes the name of one notebook and returns a transformed version of the readme file

        print(self.one_readme_file(readme_text))
        # return readme_text
