# LogInspect - A Python Tool for Parsing and Filtering Event Log Files
```
    __                ____                           __ 
   / /   ____  ____ _/  _/___  _________  ___  _____/ /_
  / /   / __ \/ __ `// // __ \/ ___/ __ \/ _ \/ ___/ __/
 / /___/ /_/ / /_/ // // / / (__  ) /_/ /  __/ /__/ /_  
/_____/\____/\__, /___/_/ /_/____/ .___/\___/\___/\__/  
            /____/              /_/                     

```
LogInspect is a Python tool designed to parse `.evtx` event log files and display filtered event data in a user-friendly, color-coded format. It allows users to easily analyze event logs by applying customizable filters such as Event ID, Keyword, Level, and Time Range.

## Features:
- **Event Log Parsing:** Easily parse `.evtx` event log files for detailed system event data.
- **Customizable Filters:** Filter events based on Event ID, keyword in Event Data, log level (Information, Warning, Error), and time range (start and end time).
- **Color-Coded Output:** Enjoy enhanced readability with color-coded output, making it easy to identify different event levels.
- **Beautified Data Display:** Event Data is formatted as tables, providing a clear and structured view of the parsed information.


## Key Benefits:
- **Quick Event Filtering:** Narrow down event logs to find specific events of interest.
- **Intuitive Display:** Easily readable tables and color-coded output for quick understanding.
- **Easy to Use:** Simple command-line interface (CLI) for quick setup and usage.


## Installation:
1. **Clone the Repository:** 
 ```bash
git clone https://github.com/YashkumarNavadiya/loginspect.git
cd loginspect
```

2. **Install Dependencies:** Create a virtual environment and install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

## Usage:
Run the tool with the following command, replacing `<file_path>` with the path to your `.evtx` file:
```bash
python loginspect.py <file_path> [--event_id EVENT_ID] [--keyword KEYWORD] [--level LEVEL] [--start_time START_TIME] [--end_time END_TIME]
```

### Parameters:
- `file_path` (Required): Path to the `.evtx` file.
- `--event_id`: Filter by a specific Event ID.
- `--keyword`: Filter by a keyword found in Event Data.
- `--level`: Filter by event level (e.g., `Information`, `Warning`, `Error`).
- `--start_time`: Filter events starting from this time (ISO format: `YYYY-MM-DDTHH:MM:SS`).
- `--end_time`: Filter events up to this time (ISO format: `YYYY-MM-DDTHH:MM:SS`).

### Example Command:
```bash
python loginspect.py logs.evtx --event_id 103 --keyword "Database" --level Warning
```
---

## Output Example

The tool outputs detailed event data in a structured and readable format:

```
============================================================
Log Name     : Application
Event ID     : 103
Source       : ESENT
Task Category: Database Operations
Level        : Warning
Version      : 0
Computer     : SERVER01
User         : SYSTEM
Timestamp    : 2024-01-15T10:30:00
Event Data   :
+-------------------+-------------------+
| Field             | Value             |
+-------------------+-------------------+
| Field1            | Value1            |
| Field2            | Value2            |
+-------------------+-------------------+
============================================================
```

---
### Contributions:
Feel free to fork the repository and submit issues or pull requests if you'd like to contribute to the development of this tool.

### License:
This tool is licensed under the MIT License. See the LICENSE file for more details.
