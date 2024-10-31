# AI Demo Sync Utilities

## Overview
Utility scripts for managing and synchronizing AI demo repositories. Includes tools for downloading information, generating lists, and syncing with Git. Designed to streamline demo content management and enhance productivity.

This repository contains a set of utilities to help synchronize data between various sources (OpenVINO repositories, Smartsheet, etc.) and a central database. The main functionality includes:

1. Extracting notebook metadata and README files from OpenVINO repositories
2. Importing data from a Smartsheet
3. Generating summaries, labels, and a JSON output based on the processed data

## Usage

1. Set up the required environment and install dependencies:
   ```
   # Create a virtual environment
   python -m venv .venv
   # Activate the virtual environment
   source venv/bin/activate
   # Install requirements
   pip install -r requirements.txt
   ```

2. Configure the necessary environment variables:
   - `DATABASE_NAME`: Name of the database to use
   - `OPENVINO_REPOSITORY`: URL of the OpenVINO repository to extract notebooks from
   - `README_NOTEBOOK_URL`: URL to fetch README files for the notebooks

3. Run the main script:
   ```
   python main.py
   ```

The script will execute the following steps:

1. Initialize the database
2. Extract notebook metadata and README files from OpenVINO repositories
3. Process data from a Smartsheet
4. Generate summaries, labels, and a JSON output

## Logging
The script logs important events, errors, and execution times to a timestamped log file in the `logs` directory. You can review these logs to monitor the pipeline's progress and troubleshoot any issues.

## Architecture
The main script is structured as a pipeline with the following steps:

1. **Initialize Database**: Ensures the required database is created.
2. **Extract Notebooks**: Fetches metadata and README files from OpenVINO repositories.
3. **Process Smartsheet**: Imports data from a Smartsheet and saves it to the database.
4. **Process AI Tasks**: Generates summaries, labels, and populates additional database tables.
5. **Generate JSON**: Exports the processed data to a JSON file.

Each step is wrapped in a decorator that handles error logging and execution time tracking.

## Customization
If you need to modify the behavior of the pipeline, you can update the corresponding methods in the `Pipeline` class. For example, you might want to change the data sources, add new processing steps, or modify the output format.

## Dependencies
The main dependencies used in this project are:
- `pandas`: For data manipulation and processing
- `sqlalchemy`: For database interactions
- `requests`: For fetching data from remote sources

Please refer to the `requirements.txt` file for the complete list of dependencies.

![repository avatar](./public/favicon.ico)

## Contact
If you have any questions or issues, feel free to reach out to the Intel® 

[Intel® Security Center]:https://www.intel.com/security

[Vulnerability Handling Guidelines]:https://www.intel.com/content/www/us/en/security-center/vulnerability-handling-guidelines.html
### License
This project is licensed under the Apache-2.0 License, as was the original OpenVINO™ Notebooks project.
