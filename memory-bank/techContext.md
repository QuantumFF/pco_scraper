# Tech Context

## Technologies Used
- **Language:** Python 3.x
- **Core Libraries:**
  - `requests`: Standard library for making HTTP GET requests to the REST API.
  - `pandas`: Used extensively for normalizing JSON structures and exporting to CSV.
  - `argparse`: Standard library for building the command-line interface.
  - `configparser`: Standard library for parsing the `config.ini` file.
  - `ast`: Standard library used (`ast.literal_eval`) to safely evaluate string representations of lists during data processing.

## Development Setup
- The project utilizes a local virtual environment (`.venv`).
- Standard execution is done via module invocation: `python -m pco_scraper.main` (or running `main.py` directly).
- A `PCOScraper.spec` file exists, indicating the project is configured to be bundled into a standalone executable using `PyInstaller`.

## Technical Constraints
- **API Rate Limits:** The script must operate within the Planning Center Online API rate limits. While not explicitly handled with sleep timers, standard execution speeds generally comply, but bulk extraction could theoretically hit limits.
- **Schema Dependency:** The data processor is highly dependent on the current structure of the PCO API responses. If Planning Center changes their JSON schema (e.g., changing where relationships are stored), the `data_processor.py` logic will need updates.

## Tool Usage Patterns
- **Execution:** Users run the script via CLI, passing endpoints via the `--endpoints` flag.
- **Configuration:** Users are encouraged to use `--create-config` to generate a `config.ini` file to securely store their App ID and Secret.
