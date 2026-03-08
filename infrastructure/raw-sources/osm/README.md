# OpenStreetMap Raw Sources

This directory holds or references OSM data for Azerbaijan. Raw PBF files are not committed to the repository. They are fetched by script and may be cached locally (gitignored).

## Source

- **Geofabrik**: https://download.geofabrik.de/europe/azerbaijan-latest-free.shp.zip or PBF (e.g. azerbaijan-latest.osm.pbf from Geofabrik).
- **License**: ODbL. Attribution required. See docs/source-licensing.md.

## Fetch Script

Run from repository root:

```bash
python scripts/fetch_osm_azerbaijan.py
```

The script will:
- Download the Azerbaijan extract from Geofabrik (or a configured URL)
- Record source timestamp and file checksum in a manifest (e.g. manifest.json)
- Optionally output to infrastructure/raw-sources/osm or a path set in config

Output path is configurable; default is infrastructure/raw-sources/osm (directory created if missing). Raw PBF is gitignored.

## Provenance

After fetch, manifest contains:
- source_name: Geofabrik Azerbaijan
- source_url: URL used
- fetched_at: ISO timestamp
- file_checksum: SHA-256 of downloaded file (optional)
- license: ODbL

## Use

Processed network is loaded into PostgreSQL/PostGIS by services/network-import. Only the processed topology and attributes are stored in the database; raw PBF is not stored in the repository.
