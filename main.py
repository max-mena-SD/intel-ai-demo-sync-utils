""" from database.database_schema import StartDatabase
from database.insert_update import InsertUpdate
import data_extraction
from utils.var_global import VarGlobal

from data_load.json_elaboration import JsonElaboration

import utils

db_name = utils.VarGlobal.DATABASE_NAME
table_name = utils.VarGlobal.TABLE_METADATA_PREMAP

print("Start...")
# Verify if the database is created
db_instance = StartDatabase(db_name)
db_status = db_instance.database_creation()

print("Step 1 database, created =", db_status)


# Load the data from OpenVINO website
# first step get the names of the repositories
repository_url = VarGlobal.OPENVINO_REPOSITORY
change_name = data_extraction.RepositoryExtraction(
    table_name, repository_url
).extract_save_notebooks()
print("Step 2 notebooks saved")

# second step get the readme of the repositories
# eliminate
reposityr_url = VarGlobal.README_NOTEBOOK_URL
data_extraction.ReadmeExtraction(reposityr_url).get_all_readme()
print("Step 3.1 notebooks inserted")


# start to work with the data from smart sheet - AI Demo Dashboard
data_extraction.SmartsheetExtractor().save_all_to_table()
print("Step 3.2 data from excel")


# update the metadata_premap table with the data from the smart sheet
# change this to go throug transformation instead of direct to database ***
InsertUpdate(VarGlobal.DATABASE_NAME).insert_ignore_smartsh()
print("Step 3.3 data from excel inserted")


print("Starting AI")
from data_transformation.add_labels import AddLabels
from data_transformation.add_summary import AddSummary
from data_transformation.populate_table import PopulateTable

# summarize the readme files first
AddSummary().process_all_summary("openvino")
print("Summary process successful")

# Fill the metadata_map table with the information from the metadata_premap table
PopulateTable().populate_premap_with_map()
print("Premap data populated")

# Add the labels and save them in the database
AddLabels().source_all_labels()
print("Labels sourced")

# Create a json file with the information from database
# JsonElaboration().json_sql_element()
JsonElaboration().sql_to_json_builder()
print("Json build")

print("... Finish.")
 """

import logging
import time
from datetime import datetime
import sys
from typing import Callable
from pathlib import Path

from database.database_schema import StartDatabase
from database.insert_update import InsertUpdate
import data_extraction
from utils.var_global import VarGlobal
from data_load.json_elaboration import JsonElaboration
import utils


class Pipeline:
    def __init__(self):
        self.db_name = utils.VarGlobal.DATABASE_NAME
        self.table_name = utils.VarGlobal.TABLE_METADATA_PREMAP
        self.setup_logging()

    def setup_logging(self):
        """Configure logging with timestamp and proper formatting."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"pipeline_{timestamp}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
        )

    def step_decorator(func: Callable) -> Callable:
        """Decorator to handle step execution with timing and error handling."""

        def wrapper(self, *args, **kwargs):
            step_name = func.__name__
            logging.info(f"Starting step: {step_name}")
            start_time = time.time()

            try:
                result = func(self, *args, **kwargs)
                execution_time = time.time() - start_time
                logging.info(
                    f"Completed step: {step_name} in {execution_time:.2f} seconds"
                )
                return result
            except Exception as e:
                logging.error(f"Error in step {step_name}: {str(e)}", exc_info=True)
                raise

        return wrapper

    @step_decorator
    def initialize_database(self):
        """Initialize and verify database creation."""
        db_instance = StartDatabase(self.db_name)
        db_status = db_instance.database_creation()
        # Si la base de datos ya existe, db_status será False, pero eso es OK
        logging.info(
            f"Database status: {'already exists' if not db_status else 'created'}"
        )
        return True  # Continuamos con el proceso independientemente del estado

    @step_decorator
    def extract_notebooks(self):
        """Extract and save notebooks from OpenVINO repository."""
        repository_url = VarGlobal.OPENVINO_REPOSITORY
        return data_extraction.RepositoryExtraction(
            self.table_name, repository_url
        ).extract_save_notebooks()

    @step_decorator
    def extract_readme(self):
        """Extract README files from notebooks."""
        repository_url = VarGlobal.README_NOTEBOOK_URL
        return data_extraction.ReadmeExtraction(repository_url).get_all_readme()

    @step_decorator
    def process_smartsheet(self):
        """Process and save smartsheet data."""
        data_extraction.SmartsheetExtractor().save_all_to_table()
        InsertUpdate(self.db_name).insert_ignore_smartsh()

    @step_decorator
    def process_ai_tasks(self):
        """Process AI-related tasks including summaries, labels, and table population."""
        from data_transformation.add_labels import AddLabels
        from data_transformation.add_summary import AddSummary
        from data_transformation.populate_table import PopulateTable

        # Generate summaries
        AddSummary().process_all_summary("openvino")

        # Populate metadata
        PopulateTable().populate_premap_with_map()

        # Process labels
        AddLabels().source_all_labels()

    @step_decorator
    def generate_json(self):
        """Generate JSON output from processed data."""
        JsonElaboration().sql_to_json_builder()

    def run_pipeline(self):
        """Execute the complete pipeline with error handling."""
        try:
            logging.info("Starting pipeline execution")
            start_time = time.time()

            # Execute pipeline steps
            self.initialize_database()
            self.extract_notebooks()
            self.extract_readme()
            self.process_smartsheet()
            self.process_ai_tasks()
            self.generate_json()

            execution_time = time.time() - start_time
            logging.info(
                f"Pipeline completed successfully in {execution_time:.2f} seconds"
            )

        except Exception as e:
            logging.error("Pipeline failed with error:", exc_info=True)
            raise


if __name__ == "__main__":
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error("Pipeline execution failed", exc_info=True)
        sys.exit(1)
