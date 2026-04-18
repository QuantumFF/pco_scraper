import argparse
import os
import sys

# Import functions/classes from your new modules
import config_manager
import api_client
import data_processor


def main():
    parser = argparse.ArgumentParser(
        description="Fetch various data from Planning Center API and save to CSVs."
    )

    # --- Config File Arguments ---
    parser.add_argument(
        "--config",
        default="config.ini",
        help="Path to the configuration file (default: %(default)s).",
    )
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Create a template config.ini file with placeholders.",
    )

    # --- API Credential Arguments (now optional if config is used) ---
    parser.add_argument(
        "--id",
        help="Your Planning Center API Application ID (overrides config file).",
    )
    parser.add_argument(
        "--secret",
        help="Your Planning Center API Application Secret (overrides config file).",
    )

    # --- URL Arguments (remain the same) ---
    parser.add_argument(
        "--check-ins-url",
        default="https://api.planningcenteronline.com/check-ins/v2/check_ins?include=locations",
        help="Base URL for Check-Ins API (default: %(default)s).",
    )
    parser.add_argument(
        "--people-url",
        default="https://api.planningcenteronline.com/people/v2/people",
        help="Base URL for People API (default: %(default)s).",
    )
    parser.add_argument(
        "--tabs-url",
        default="https://api.planningcenteronline.com/people/v2/tabs",
        help="Base URL for Tabs API (default: %(default)s).",
    )
    parser.add_argument(
        "--field-data-url",
        default="https://api.planningcenteronline.com/people/v2/field_data",
        help="Base URL for Field Data API (default: %(default)s).",
    )
    parser.add_argument(
        "--field-definitions-url",
        default="https://api.planningcenteronline.com/people/v2/field_definitions",
        help="Base URL for Field Definitions API (default: %(default)s).",
    )
    parser.add_argument(
        "--start-date",
        help="Optional start date for check-ins (YYYY-MM-DD). Not applicable to all endpoints.",
        default=None,
    )
    parser.add_argument(
        "--endpoints",
        nargs="*",
        choices=[
            "check_ins",
            "people",
            "tabs",
            "field_data",
            "field_definitions",
            "all",
        ],
        default=["all"],
        help="Specify which endpoints to scrape (e.g., 'check_ins people'). Use 'all' to scrape everything (default: all). "
        "Note: 'people' refers to /people/v2/people, not a relationship.",
    )
    parser.add_argument(
        "--output-folder",
        default="output",
        help="Name of the folder to save output CSVs (default: %(default)s).",
    )

    args = parser.parse_args()

    # Handle --create-config argument
    if args.create_config:
        config_manager.create_config_template(args.config)
        sys.exit(0)  # Exit after creating config file

    # Load credentials
    app_id, app_secret = config_manager.load_credentials(
        args.id, args.secret, args.config
    )

    # Final check for credentials
    if not app_id or not app_secret:
        parser.error(
            "API credentials (ID and Secret) are required. "
            "Provide them via --id and --secret, or set them in a config file (--config). "
            "Use --create-config to generate a template."
        )

    output_folder = args.output_folder

    # Define all available endpoints and their corresponding URLs and default parameters
    all_endpoints = {
        "check_ins": {
            "url": args.check_ins_url,
            "params": {"per_page": 100},
        },
        "people_v2": {
            "url": args.people_url,
            "params": {"per_page": 100},
        },
        "tabs": {
            "url": args.tabs_url,
            "params": {"per_page": 100},
        },
        "field_data": {
            "url": args.field_data_url,
            "params": {"per_page": 100},
        },
        "field_definitions": {
            "url": args.field_definitions_url,
            "params": {"per_page": 100},
        },
    }

    # Determine which endpoints to scrape based on --endpoints argument
    endpoints_to_scrape = []
    if "all" in args.endpoints:
        endpoints_to_scrape = list(all_endpoints.keys())
    else:
        for ep in args.endpoints:
            if ep == "people":
                endpoints_to_scrape.append("people_v2")
            else:
                endpoints_to_scrape.append(ep)

    for endpoint_name in endpoints_to_scrape:
        endpoint_info = all_endpoints[endpoint_name]
        current_base_url = endpoint_info["url"]
        params = endpoint_info["params"]

        # Ensure 'include=locations' is present for check_ins URL if not already there
        if (
            endpoint_name == "check_ins"
            and "include=locations" not in current_base_url
        ):
            current_base_url += "&include=locations" if "?" in current_base_url else "?include=locations"


        initial_url_with_params = (
            f"{current_base_url}&offset=0&per_page={params['per_page']}"
            if "?" in current_base_url
            else f"{current_base_url}?offset=0&per_page={params['per_page']}"
        )

        if endpoint_name == "check_ins" and args.start_date:
            initial_url_with_params = (
                f"{initial_url_with_params}&where[created_at][gte]={args.start_date}"
            )

        print(f"\n--- Scraping {endpoint_name.replace('_v2', ' people')} endpoint ---")
        all_records = api_client.fetch_all_paginated_data(
            initial_url_with_params, app_id, app_secret, endpoint_name
        )

        print(f"  Successfully fetched {len(all_records)} records for '{endpoint_name}'.")
        data_processor.process_and_save_data(
            all_records, endpoint_name.replace("_v2", "people"), output_folder
        )


if __name__ == "__main__":
    main()