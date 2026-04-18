# System Patterns

## System Architecture
The application is a modular command-line interface (CLI) Python script structured into distinct functional components:
- **`main.py`:** The entry point. Handles `argparse` configuration, reads user inputs, and orchestrates the flow between configuration, API fetching, and data processing.
- **`config_manager.py`:** Responsible for resolving API credentials. It checks command-line arguments first, falling back to a `config.ini` file if arguments are omitted. It also handles generating configuration templates.
- **`api_client.py`:** Manages all HTTP interactions with the Planning Center API. It includes robust logic for iterating over paginated API responses by following the `links.next` URL provided in the API payload.
- **`data_processor.py`:** The core transformation engine. It receives raw JSON arrays and utilizes `pandas` to flatten nested attributes and relationships into standard DataFrame columns before exporting to CSV.

## Key Technical Decisions
- **Pandas for ETL:** Chosen for its powerful `json_normalize` capabilities and easy CSV export, significantly reducing the amount of manual iteration required to flatten nested data.
- **Explicit Schema Definition:** `data_processor.py` defines explicit `meta_fields` for specific endpoints (like `check_ins`, `people_v2`). This ensures that only relevant data is extracted and mapped correctly, though it requires manual updates if the API schema evolves.
- **Column Renaming:** A structured renaming mapping is applied to strip verbose JSON API prefixes (e.g., changing `relationships_person_data_id` to a cleaner `person_id`).

## Design Patterns in Use
- **Modularization:** Distinct separation of concerns (Configuration, Extraction, Transformation).
- **Fail-Safe Iteration:** Pagination loops check for `None` or missing `data` keys to break gracefully rather than throwing unhandled exceptions.

## Component Relationships
`main.py` -> calls `config_manager` to get credentials.
`main.py` -> calls `api_client` with credentials and URLs to get raw data.
`main.py` -> passes raw data to `data_processor` to generate CSVs in the output directory.
