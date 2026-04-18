# Product Context

## Why this project exists
Organizations utilizing Planning Center Online (PCO) frequently need to perform advanced, custom reporting or data analysis that falls outside the platform's native capabilities. This scraper provides an automated way to extract bulk data to perform these operations in external tools like Excel, Tableau, or custom dashboards.

## Problems it solves
- **Pagination Management:** The PCO API paginates results. This tool automatically follows pagination links to fetch all available records without manual intervention.
- **Complex JSON Normalization:** PCO API responses contain deeply nested dictionaries and relationships (e.g., person avatars, check-in locations, event periods). The tool flattens these into readable, tabular CSV files, saving users from writing complex parsing logic.
- **Authentication Handling:** Provides a seamless way to authenticate using App ID and Secret via either secure config files or command-line arguments.

## How it should work
1. The user configures their PCO API credentials (via `config.ini` or CLI arguments).
2. The user runs `main.py` specifying the target endpoints (e.g., `--endpoints check_ins people`).
3. The script queries the endpoints, handles pagination, and passes the raw JSON records to the data processor.
4. The processor normalizes the nested dictionaries and relationships using Pandas.
5. Clean, flattened CSV files are generated in the specified `output` folder.

## User Experience Goals
- **Simplicity:** Provide a straightforward CLI experience with helpful default values.
- **Transparency:** Output clear console logs detailing pagination progress, record counts, and saved file locations.
- **Flexibility:** Allow users to define date ranges (for check-ins) and select specific endpoints to minimize unnecessary API calls.
