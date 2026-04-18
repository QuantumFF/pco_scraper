# Progress

## Current Status
- The project is fully functional and stable for its intended scope.
- Memory Bank initialized on initial analysis.

## What Works
- **Authentication:** Loading credentials from CLI args or `config.ini`.
- **API Scraping:** Fetching data from Check-Ins, People, Tabs, Field Data, and Field Definitions endpoints.
- **Pagination:** Automatically navigating through all pages of the API responses.
- **Data Transformation:** Normalizing complex nested JSON and extracting specific relationships (like location IDs).
- **Exporting:** Saving cleaned, tabular data to CSV files in an `output` directory.

## What's Left to Build
- No active roadmap or pending features. The core objective of extracting PCO data to CSV is met.

## Known Issues
- No explicit API rate limit handling (e.g., retries on 429 Too Many Requests).
- Schema mapping is hardcoded; unannounced API changes from Planning Center could break the normalizer.

## Evolution of Project Decisions
- The use of `pandas` appears to be a core decision to handle the heavy lifting of JSON normalization, replacing what would otherwise be complex, nested dictionary iterations.
- Added custom logic to safely parse stringified lists (`ast.literal_eval`) in the locations data, indicating a past issue with data types returned by the normalization process.
- Implemented global newline replacement (`\n`, `\r` to `, `) in `data_processor.py` to prevent multi-line strings from breaking the structure of the exported CSV files.
