# Retrieving GEOData

Python for Everybody — Chapter 16 / Module 5 worked example. This project geocodes a
list of place names using the py4e OpenStreetMap proxy, stores the results in a SQLite
database, exports them to JavaScript, and visualizes them on an OpenLayers map.

## Files

| File | Purpose |
|------|---------|
| `where.data` | Input — one place name per line. Line 1 is the custom added location. |
| `geoload.py` | Reads `where.data`, geocodes each entry via the API, stores results in `opengeo.sqlite`. Skips entries already in the database. |
| `geodump.py` | Reads `opengeo.sqlite` and writes `where.js` with `[lat, lng, name]` rows. |
| `where.js` | Generated JavaScript data consumed by the map. |
| `where.html` | Opens in a browser to visualize the locations on an OpenStreetMap map. |
| `opengeo.sqlite` | Cache database. Delete it to start the whole process from scratch. |
| `README.txt` | Original assignment notes shipped in `opengeo.zip`. |

## Requirements

- Python 3 (standard library only — `urllib`, `sqlite3`, `json`)
- A browser to open `where.html`
- Optional: [DB Browser for SQLite](https://sqlitebrowser.org/) to inspect the database

## Running

On Windows, use **PowerShell** and set UTF-8 first, otherwise `geodump.py` can crash
with a `UnicodeEncodeError` on accented place names:

```powershell
$env:PYTHONIOENCODING="utf-8"
```

Then:

```powershell
python geoload.py    # geocode entries into opengeo.sqlite
python geodump.py    # export opengeo.sqlite -> where.js
```

Open `where.html` in a browser to view the map. Hover or click a pin to see the
address the geocoder returned.

## Notes

- `geoload.py` caches results, so re-running only fetches new entries. To force a
  fresh lookup of a single entry, delete its row:

  ```powershell
  python -c "import sqlite3; c=sqlite3.connect('opengeo.sqlite'); c.execute(\"DELETE FROM Locations WHERE address like '%Mohatta%'\"); c.commit()"
  ```

- To rebuild everything from zero, delete `opengeo.sqlite` and re-run both scripts.
- `geoload.py` stops after 100 API lookups per run (the `count > 100` guard); run it
  again to continue where it left off.
- The added custom location must be a real place run through `geoload.py` — do not
  insert rows into the database by hand, as the geocoding output is the required
  evidence for this assignment.
