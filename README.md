# Asset Dashboard

A web-based dashboard for scanning and visualizing 3D asset pipelines. Built with Python and Flask.

## Install

```bash
pip install flask
```

## Run

```bash
python app.py
```

Then open `http://127.0.0.1:5000/dashboard` in your browser.

## Usage

Enter a folder path in the input field and hit Scan. The dashboard will show:
- Total asset count
- Breakdown by file type
- Naming errors (uppercase, spaces)
- Duplicate assets across subdirectories

## Routes

- `/dashboard` — browser dashboard
- `/scan` — raw JSON output