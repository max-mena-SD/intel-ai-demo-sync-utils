import sys
import os
import unittest

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.download_readme import ReadmeDownloader


class TestReadmeDownloader(unittest.TestCase):
    def test_download_readme(self):
        path_name = "data/readme_files/test_readme.md"
        downloader = ReadmeDownloader(path_name)
        notebook_name = "3D-pose-estimation-webcam"
        downloader.download_readme(notebook_name)
        self.assertTrue(os.path.exists(path_name))
        # Clean up
        if os.path.exists(path_name):
            os.remove(path_name)


if __name__ == "__main__":
    unittest.main()
