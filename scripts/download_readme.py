import requests


class ReadmeDownloader:
    def __init__(self, path_name):
        self.path_name = path_name

    def download_readme(self, notebook_name):
        url = f"https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/notebooks/{notebook_name}/README.md"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            with open(self.path_name, "wb") as file:
                file.write(response.content)
            print(f"Readme file for {notebook_name} saved successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {notebook_name}: {e}")
        except IOError as e:
            print(f"Error saving file {self.path_name}: {e}")
