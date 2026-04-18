# Active Context

## Current Work Focus
- Initializing the Memory Bank based on a comprehensive analysis of the existing codebase.
- The project is currently in a stable, functional state for scraping and exporting PCO data.

## Recent Changes
- Fixed a bug in `data_processor.py` where newline characters (`\n`, `\r`) in raw data caused structural issues in the exported CSV files by replacing them with commas.
- Initial project analysis and documentation.

## Next Steps
- Await user directives for new feature development, bug fixes, or enhancements.

## Active Decisions and Considerations
- **Data Normalization Strategy:** Using `pandas.json_normalize` with explicitly defined `meta_fields` to flatten the PCO JSON responses. This requires maintenance if the PCO API schema changes.
- **Relationship Extraction:** Specific hardcoded logic exists in `data_processor.py` to extract location types and IDs from the `relationships_locations_data` list. This approach is targeted and might need expansion if other complex relationships are required.
- **Configuration:** Preferring a `config.ini` approach for credential management to prevent secrets from appearing in command-line histories, but retaining CLI args for flexibility.

## Important Patterns and Preferences
- **Separation of Concerns:** Keep API fetching (`api_client.py`), data manipulation (`data_processor.py`), and CLI orchestration (`main.py`) strictly separated.
- **Graceful Degradation:** The script catches RequestExceptions and handles missing data keys without crashing the entire extraction process.

## Learnings and Project Insights
- The Planning Center API heavily utilizes JSON API standards, making relationships verbose. The custom logic to map these to standard foreign-key style columns (e.g., `person_id`, `event_id`) is central to the value this scraper provides.
