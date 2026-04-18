# PCO Scraper

A command-line tool to extract and format data from the Planning Center Online (PCO) API.

## Setup Instructions

### 1. Create Virtual Environment
First, create a new Python virtual environment in the project directory:
```bash
python3 -m venv .venv
```

### 2. Activate Virtual Environment
Depending on your operating system, activate the virtual environment:

**Linux / macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.\.venv\Scripts\Activate
```

### 3. Install Requirements
Install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```

---

## Usage

### Generate Configuration
You can generate a template `config.ini` file from the command line:
```bash
python main.py --create-config
```
*(Note: Use `python main.py` or `./PCOScraper.py` depending on your execution preference).*

---

## Packaging

To bundle the application into a standalone executable using PyInstaller, run:
```bash
pyinstaller PCOScraper.spec
```