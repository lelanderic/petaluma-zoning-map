# Pipeline (reference only)

These are the working scripts that prepared `src/assets/` from the City's files. They were run step by step, with intermediate files and hand checks in between, so they are a record of the method and not a one-command rebuild. Paths inside them point at a scratch folder.

| Script | What it did |
|---|---|
| `classify_zones.py` | Rendered Exhibit C page 2 at 300 dpi, matched each pixel to a legend color (including pixels blended with parcel lines), and wrote the zone lookup grid, the cleaned base image and the per-zone pixel counts. |
| `trace_overlays.py` | Traced the overlay areas from Exhibit C page 3 by symbol color. |
| `geo.py`, `streets.txt` | Key vertices of major streets from the City's street layer (California State Plane Zone II, feet) and the fit of those coordinates to map pixels: about 11.65 feet per pixel, north up. |
| `place_street_labels.py` | Placed street labels and angles along those centerlines. |
| `rasterize_city_layers.py` | Drew the City's General Plan 2050 parcels and 2008 PUD/PCD polygons onto the map grid, and compared General Plan designations with the zones read from the map colors. |

Inputs not stored in this repository: the two City PDFs (Exhibits B and C) and the GIS download (`petaluma_gis.json`, about 3.8 MB).

Python packages used: numpy, scipy, Pillow, opencv-python. `pdftoppm` and `pdftotext` (poppler) were used to render and read the PDFs.
