import database
import data_extraction
from utils import Config


import utils

# # Verify if the database is created
# database.StartDatabase("ai_demo_metadata.db").check_database()

# # Load the data from OpenVINO website
# # first step get the names of the repositories
# repository_url = Config().OPENVINO_REPOSITORY
# table_name = "metadata_premap"
# change_name = data_extraction.RepositoryExtraction(
#     table_name, repository_url
# ).extract_save_notebooks()

# # second step get the readme of the repositories
# # eliminate
reposityr_url = Config().README_NOTEBOOK_URL
data_extraction.ReadmeExtraction(reposityr_url).get_all_readme()
