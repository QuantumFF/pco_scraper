import requests
import sys


def fetch_single_page(url, app_id, app_secret):
    """Fetches data from a single API URL."""
    try:
        response = requests.get(url, auth=(app_id, app_secret))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}", file=sys.stderr)
        return None


def fetch_all_paginated_data(initial_url, app_id, app_secret, endpoint_name):
    """Fetches all paginated data from an endpoint."""
    current_url = initial_url
    all_records = []
    page_count = 0

    while current_url:
        print(f"  Fetching page {page_count + 1} from: {current_url}")
        data = fetch_single_page(current_url, app_id, app_secret)

        if data is None:
            print(
                f"  Failed to retrieve data for {endpoint_name}. Exiting pagination for this endpoint.",
                file=sys.stderr,
            )
            break

        if "data" in data and isinstance(data["data"], list):
            all_records.extend(data["data"])
        else:
            print(
                f"  Warning: 'data' key not found or is not a list in response from {current_url}. Stopping for this endpoint.",
                file=sys.stderr,
            )
            break

        if "links" in data and "next" in data["links"] and data["links"]["next"]:
            current_url = data["links"]["next"]
            page_count += 1
        else:
            current_url = None

    return all_records