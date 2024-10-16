import database
import data_extraction
from utils import Config
from utils.var_global import VarGlobal
from data_transformation.add_summary import AddSummary

import utils

# db_name = utils.Config.DATABASE_NAME
# table_name = utils.Config.TABLE_METADATA_PREMAP

# # Verify if the database is created
# database.StartDatabase(db_name).check_database()

# # Load the data from OpenVINO website
# # first step get the names of the repositories
# repository_url = Config().OPENVINO_REPOSITORY
# change_name = data_extraction.RepositoryExtraction(
#     table_name, repository_url
# ).extract_save_notebooks()

# # second step get the readme of the repositories
# # eliminate
# reposityr_url = Config().README_NOTEBOOK_URL
# data_extraction.ReadmeExtraction(reposityr_url).get_all_readme()


# # start to work with the data from smart sheet - AI Demo Dashboard
# data_extraction.SmartsheetExtractor().save_all_to_table()

# # update the metadata_premap table with the data from the smart sheet
# # change this to go throug transformation instead of direct to database ***
# database.InsertUpdate(VarGlobal.DATABASE_NAME).update_premap_smartsheet()


# summarize the readme files first
print(AddSummary().summarize_openvino())
