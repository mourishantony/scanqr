# Flask LinkedIn QR Scanner

This project is a Flask web app with two pages:

1. **QR Scan Page**: Uses your camera to scan LinkedIn profile QR codes. When a LinkedIn profile is detected, it saves the profile link and name to a database.
2. **Profiles Page**: Displays all scanned LinkedIn profiles (name and link) from the database.

## Setup


1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app:
   ```sh
   python app.py
   ```
3. Open your browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Features
- Camera-based QR code scanning (LinkedIn profiles only)
- Stores scanned profile name and link in a local SQLite database
- View all scanned profiles on a separate page

## File Structure
- `app.py` — Main Flask app
- `templates/scan.html` — QR scanner page
- `templates/profiles.html` — Profiles display page
- `requirements.txt` — Python dependencies

## Notes
- Only LinkedIn profile QR codes are accepted.
- Name is extracted from the LinkedIn URL (may not be the full real name).

---

Replace this README with more details as needed.
