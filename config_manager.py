import configparser
import os
import sys


def create_config_template(config_path):
    """Creates a template config.ini file."""
    config = configparser.ConfigParser()
    config["PCO_API"] = {
        "app_id": "YOUR_APP_ID_HERE",
        "app_secret": "YOUR_APP_SECRET_HERE",
    }
    try:
        with open(config_path, "w") as configfile:
            config.write(configfile)
        print(f"Template config file created at '{config_path}'.")
        print("Please edit this file with your actual Planning Center API credentials.")
        print("You can then run the script without --id and --secret like: python -m pco_scraper.main")
    except IOError as e:
        print(f"Error creating config file '{config_path}': {e}", file=sys.stderr)


def load_credentials(cmd_id, cmd_secret, config_path):
    """
    Loads API credentials from command line or config file.
    Command line arguments take precedence.
    """
    app_id = cmd_id
    app_secret = cmd_secret

    if app_id is None or app_secret is None:
        config = configparser.ConfigParser()
        try:
            config.read(config_path)
            if "PCO_API" in config:
                app_id = app_id or config["PCO_API"].get("app_id")
                app_secret = app_secret or config["PCO_API"].get("app_secret")
            else:
                print(
                    f"Warning: Section [PCO_API] not found in '{config_path}'.",
                    file=sys.stderr,
                )
        except Exception as e:
            print(
                f"Warning: Could not read config file '{config_path}': {e}",
                file=sys.stderr,
            )
            print("Ensure the file exists and is correctly formatted.", file=sys.stderr)

    return app_id, app_secret