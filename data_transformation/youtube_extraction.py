import requests
import json


class YoutubeExtraction:
    def youtube_connection(self, video_id):
        """"""
        try:
            api_key = "AIzaSyDTc0PZNUDWx0JUa-v7rwCtHogyEWbzA7E"
            url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet"
            response = requests.get(url)
            data = response.json()

            return data
        except Exception as e:
            raise ValueError(
                "An error occurred while reading the JSON file. Getting data from youtube"
            )

    def youtube_retrieval(self, path_file):

        file_path = "../data/test_youtube.json"  # "./data/test_youtube.json"
        try:
            youtube_metadata_list = []
            with open(path_file, "r") as file:
                data = json.load(file)

            for item in data:
                metadata_registry = self.youtube_connection(str(item["Video_id"]))
                if metadata_registry["items"]:
                    print(metadata_registry["items"])
                    youtube_metadata_list.append(metadata_registry)

            print("YouTube metadata saved successfully.")

            with open(file_path, "w") as file:
                json.dump(youtube_metadata_list, file, indent=4)

        except Exception as e:
            raise ValueError(
                "An error occurred while reading the JSON file. Saving youtube information"
            )
