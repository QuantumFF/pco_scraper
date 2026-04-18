# Project Brief

This project is `pco_scraper`, a command-line Python application designed to extract data from the Planning Center Online (PCO) API. It queries various API endpoints, normalizes the JSON responses, and exports the structured data into CSV files.

## Core Requirements & Goals
- Extract paginated data reliably from the PCO API.
- Support multiple specific endpoints: Check-Ins, People, Tabs, Field Data, and Field Definitions.
- Flatten deeply nested JSON structures and relationships into analytical-friendly tabular formats.
- Save the results locally as CSV files.
- Provide a clear, easy-to-use Command Line Interface with flexible configuration (arguments vs `config.ini`).

## Scope
The tool acts as a dedicated ETL (Extract, Transform, Load) script tailored specifically to Planning Center Online's data schema. It handles API communication, data transformation, and file generation, serving as an intermediate step for users wanting to run custom analytics on their PCO data.
