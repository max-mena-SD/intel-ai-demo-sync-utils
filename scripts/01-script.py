import json
import download_readme as dr
import extract_to_json as ej
import log_progress as lp

# Initialize logger and extractor
log_file = "./docs/log/"
output_path = "./data/Openvino_data.json"
logger = lp.LogProcess(log_file).log
extractor = ej.ExtractToJSON(output_path)

# Extract and process notebooks
rows = extractor.extract_notebooks()
data = extractor.parse_notebooks(rows)
extractor.load_to_json(data)

# Read and process the JSON file
try:
    with open(output_path, "r") as file:
        notebook_data = json.load(file)
    logger(f"Data read from {output_path}")
except Exception as e:
    logger(f"Error reading the JSON file: {e}")

# Download readme files for each notebook
for notebook_name in notebook_data.keys():
    try:
        path_name = f"./data/readme_files/{notebook_name}.md"
        downloader = dr.ReadmeDownloader(path_name)
        downloader.download_readme(notebook_name)
        logger(f"Readme file saved for {notebook_name}")
    except Exception as e:
        logger(f"Error downloading {notebook_name}: {e}")
