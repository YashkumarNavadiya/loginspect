import argparse
import os
from Evtx.Evtx import Evtx
import xmltodict
import random
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)


# Define the logo
logo = r"""
    __                ____                           __
   / /   ____  ____ _/  _/___  _________  ___  _____/ /_
  / /   / __ \/ __ `// // __ \/ ___/ __ \/ _ \/ ___/ __/
 / /___/ /_/ / /_/ // // / / (__  ) /_/ /  __/ /__/ /_
/_____/\____/\__, /___/_/ /_/____/ .___/\___/\___/\__/
            /____/              /_/
"""

# List of colorama color options
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTGREEN_EX]
logocolor = None
# Function to display the logo in a random color
def print_logo():
    global logocolor
    logocolor = random.choice(colors)
    print(logocolor + logo)

def show_usage():
    """
    Displays the usage information for the script.
    """
    usage_text = """
    Usage: python LogInspect.py <file_path> [options]

    Arguments:
    <file_path>          Path to the .evtx file to parse.

    Options:
    --event_id <ID>      Filter by specific Event ID (integer).
    --keyword <keyword>  Filter by keyword in Event Data (string).
    --level <level>      Filter by event level (e.g., Information, Warning, Error).
    --start_time <time>  Filter events starting from this time (ISO format: YYYY-MM-DDTHH:MM:SS).
    --end_time <time>    Filter events up to this time (ISO format: YYYY-MM-DDTHH:MM:SS).

    Example:
    python LogInspect.py logs.evtx --event_id 4624 --level Information --start_time 2024-01-01T00:00:00 --end_time 2024-12-31T23:59:59
    """

    print(logocolor + usage_text)

def filter_event_data(event_data):
    """
    Filters out unwanted fields from the parsed XML event data.
    """
    unwanted_fields = {"Event ID", "Raw Event Data"}  # Fields to exclude
    return {key: value for key, value in event_data.items() if key not in unwanted_fields}

def print_event_details(event):
    """
    Prints the event details after filtering unwanted data.
    """
    # Filter out unwanted fields
    filtered_event = filter_event_data(event)

    # Format and display output
    println()
    # print("============================================================")
    for key, value in filtered_event.items():
        print(f"{key:<15}: {value}")
    # print("============================================================")

def beautify_event_data(event_data):
    """
    Beautifies the event data for better readability.

    Parameters:
    - event_data (dict): Event data dictionary.

    Returns:
    - str: Beautified event data as a formatted table string or a message.
    """
    if event_data is None:
        return "No Event Data Found."
    elif isinstance(event_data.get("Data"), list):
        # Data is a list of key-value pairs
        table = [[data.get("@Name", "N/A"), data.get("#text", "N/A")] for data in event_data["Data"]]
        return tabulate(table, headers=["Field", "Value"], tablefmt="grid")
    elif isinstance(event_data.get("Data"), dict):
        # Data is a single dictionary
        table = [[k, v] for k, v in event_data["Data"].items()]
        return tabulate(table, headers=["Field", "Value"], tablefmt="grid")
    elif isinstance(event_data.get("Data"), str):
        # Data is a raw string (likely structured data)
        return event_data["Data"]
    else:
        return "No Event Data Found."

def display_event(log_name, event_id, source, task_category, level, version, computer, user, timestamp, event_data):
    """
    Display event details with color formatting and beautified Event Data.

    Parameters:
    - log_name (str): Log name.
    - event_id (str): Event ID.
    - source (str): Event source.
    - task_category (str): Task category.
    - level (str): Event level.
    - user (str): User ID.
    - timestamp (str): Event timestamp.
    - event_data (dict): Event data dictionary.

    Returns:
    - None
    """

    # Define color scheme based on level
    level_colors = {
        "Information": Fore.GREEN,
        "Warning": Fore.YELLOW,
        "Error": Fore.RED,
    }

    color = level_colors.get(level, Fore.WHITE)  # Default to white if no match
    print(color + "=" * 60)
    print("\n")
    print(f"{logocolor}Log Name     :{Style.RESET_ALL} {log_name}")
    print(f"{logocolor}Event ID     :{Style.RESET_ALL} {event_id}")
    print(f"{logocolor}Source       :{Style.RESET_ALL} {source}")
    print(f"{logocolor}Task Category:{Style.RESET_ALL} {task_category}")
    print(f"{logocolor}Level        :{Style.RESET_ALL}{color} {level}{Style.RESET_ALL}")
    print(f"{logocolor}Version      :{Style.RESET_ALL} {version}")
    print(f"{logocolor}Computer     :{Style.RESET_ALL} {computer}")
    print(f"{logocolor}User         :{Style.RESET_ALL} {user}")
    print(f"{logocolor}Timestamp    :{Style.RESET_ALL} {timestamp}")
    print(f"{logocolor}Event Data   :")
    print(beautify_event_data(event_data))
    print("\n")

def parse_evtx_file(file_path, event_id=None, keyword=None, level=None, start_time=None, end_time=None):
    """
    Parse an .evtx file and filter events based on optional parameters.

    Parameters:
    - file_path (str): Path to the .evtx file.
    - event_id (int): Filter by specific Event ID.
    - keyword (str): Filter by keyword in Event Data.
    - level (str): Filter by event level.
    - start_time (str): Filter events starting from this time (ISO format: YYYY-MM-DDTHH:MM:SS).
    - end_time (str): Filter events up to this time (ISO format: YYYY-MM-DDTHH:MM:SS).

    Returns:
    - None
    """
    if not os.path.exists(file_path):
        print(f"{Fore.RED}File not found: {file_path}")
        return

    try:
        with Evtx(file_path) as evtx_file:
            print(f"{Fore.CYAN}Parsing {file_path}...\n")

            for record in evtx_file.records():
                xml_data = record.xml()
                event = xmltodict.parse(xml_data)

                # Extract necessary fields
                event_details = event["Event"]
                system_data = event_details.get("System", {})
                event_data = event_details.get("EventData", None)

                log_name = system_data.get("Channel", "Unknown Log")
                event_time = system_data.get("TimeCreated", {}).get("@SystemTime", "")
                current_event_id = system_data.get("EventID", {}).get("#text", system_data.get("EventID", ""))
                event_source = system_data.get("Provider", {}).get("@Name", "Unknown Source")
                task_category = system_data.get("Task", "Unknown Task")
                event_level = system_data.get("Level", "Unknown Level")
                version = system_data.get("Version", "Unknown Version")
                computer = system_data.get("Computer", "Unknown Domain")
                user = system_data.get("Security", {}).get("@UserID", "Unknown User")

                # Filtering logic
                if event_id and str(event_id) != str(current_event_id):
                    continue
                if keyword and keyword.lower() not in str(event_data).lower():
                    continue
                if level and level.lower() != event_level.lower():
                    continue
                if start_time and event_time < start_time:
                    continue
                if end_time and event_time > end_time:
                    continue

                # Display event details
                display_event(
                    log_name=log_name,
                    event_id=current_event_id,
                    source=event_source,
                    task_category=task_category,
                    level=event_level,
                    version=version,
                    computer=computer,
                    user=user,
                    timestamp=event_time,
                    event_data=event_data if event_data else {},
                )
    except Exception as e:
        print(f"{Fore.RED}Error parsing the file: {str(e)}")

def main():
    """
    Main function to handle command-line arguments and parse the .evtx file.
    """
    # List of colorama color options (same as logo colors)
    logo_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

    # Randomly choose the color for the logo
    logocolor = random.choice(logo_colors)

    # Define the parser
    parser = argparse.ArgumentParser(description="Parse .evtx files with optional filters.")

    # Arguments for file path and filters
    parser.add_argument("file_path", help="Path to the .evtx file", type=str, nargs="?", default=None)
    parser.add_argument("--event_id", type=int, help="Filter by Event ID (integer)")
    parser.add_argument("--keyword", type=str, help="Filter by keyword in Event Data (string)")
    parser.add_argument("--level", type=str, help="Filter by event level (e.g., Information, Warning, Error)")
    parser.add_argument("--start_time", type=str, help="Filter events starting from this time (ISO format: YYYY-MM-DDTHH:MM:SS)")
    parser.add_argument("--end_time", type=str, help="Filter events up to this time (ISO format: YYYY-MM-DDTHH:MM:SS)")

    # Parse the arguments
    args = parser.parse_args()

    # Display the logo with random color
    print_logo()

    # Show usage instructions if no file path is provided
    if not args.file_path:
        show_usage()
        return

    # Print command-line argument descriptions with the same logocolor as the logo
    print(logocolor + "\n[Arguments]".center(60, "="))
    print(logocolor + f"File Path     : {args.file_path}")
    if args.event_id:
        print(logocolor + f"Event ID      : {args.event_id}")
    if args.keyword:
        print(logocolor + f"Keyword       : {args.keyword}")
    if args.level:
        print(logocolor + f"Level         : {args.level}")
    if args.start_time:
        print(logocolor + f"Start Time    : {args.start_time}")
    if args.end_time:
        print(logocolor + f"End Time      : {args.end_time}")

    # Parse the evtx file with the provided filters
    parse_evtx_file(
        file_path=args.file_path,
        event_id=args.event_id,
        keyword=args.keyword,
        level=args.level,
        start_time=args.start_time,
        end_time=args.end_time,
    )


if __name__ == "__main__":
    main()
