import json
import summary_classify as sc
import log_progress as lp

# Initialize logger and classifier
log_file = "./docs/log/"
output_path = "./data/Openvino_data.json"
logger = lp.LogProcess(log_file).log
classifier = sc.SummaryClassify()
logger("Classifier has been initialized")

# Load notebook data
try:
    with open(output_path, "r") as file:
        notebook_data = json.load(file)
    logger(f"Data read from {output_path}")
except Exception as e:
    logger(f"Error reading JSON file: {e}")
    notebook_data = {}  # Initialize as empty dict to avoid further errors

# Process each notebook
for notebook_process in notebook_data.keys():
    try:
        with open(f"./data/readme_files/{notebook_process}.md", "r") as file:
            readme_text = file.read()
        logger(f"{notebook_process} size: {len(readme_text)} characters")

        summary = classifier.to_sumarize(readme_text)
        result = classifier.clasify_all(summary=summary)

        if result is None:
            result = {"error": "No results found"}
            logger(f"{notebook_process} did not return a classification!")

        notebook_data[notebook_process] = result
        logger(f"Notebook: {notebook_process} has been processed")

    except Exception as e:
        logger(f"{notebook_process} Error: {e}")

# Save updated notebook data
try:
    with open(output_path, "w") as file:
        json.dump(notebook_data, file)
    logger(f"Data saved to {output_path}")
except Exception as e:
    logger(f"Error saving JSON file: {e}")
