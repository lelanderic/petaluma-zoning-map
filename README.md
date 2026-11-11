# Petaluma Proposed Zoning Map

An unofficial, clickable version of the City of Petaluma's proposed citywide zoning map (Exhibit C, draft of November 9, 2026).

The City's map uses 37 colors and no street names. This version lets you:

- **Hover** to see a zone's plain name and a one-line description.
- **Click** to pin a spot and see density, height limit, floor area ratio, the former zone name, the General Plan land use for that parcel, and where the rules sit in the ordinance. The rest of the map fades so you can see where else that zone applies.
- **Find a zone** by clicking it in the legend.
- **Switch to 7 simple groups** for a quieter picture.
- **Turn on overlays**: flood plain, historic districts, senior mobile home parks, fairgrounds, T6-Open.
- **See PUD and PCD names** and the General Plan land use underneath them.

**This is not a City product and the zoning it shows has not been adopted. See [CAVEATS.md](CAVEATS.md).** The same caveats are available in the map under "About & caveats".

## Sources

| What | Source |
|---|---|
| Zone boundaries, overlays | City of Petaluma, Attachment 1, Exhibit C, Citywide Zoning Map (November 9, 2026) |
| Zone names, descriptions, standards | City of Petaluma, Attachment 1, Exhibit B, Amendments in Clean (November 9, 2026) |
| General Plan land use, street names, PUD/PCD names | City of Petaluma public GIS, `maps.cityofpetaluma.net`, downloaded November 10, 2026 |

## What is in this repository

```
public/index.html      The map. One self-contained file; this is what gets deployed.
CAVEATS.md             What the map can and cannot tell you.
src/template.html      Page layout, styles and script.
src/zones.py           Zone text, overlay text and street labels. Edit this to fix wording.
src/build.py           Assembles public/index.html from the template, zones.py and assets.
src/assets/            Prepared map image and lookup grids.
pipeline/              Reference scripts used to prepare the assets from the City's files.
```

## Changing the text

Edit `src/zones.py` or `src/template.html`, then rebuild:

```
python3 src/build.py
```

This needs only Python 3. Commit the regenerated `public/index.html`.

The scripts in `pipeline/` are the working scripts that turned the City's PDF and GIS layers into the files in `src/assets/`. They are kept for the record and are not a one-command rebuild. See `pipeline/README.md`.

## Deploying on Cloudflare Pages

1. Push this repository to GitHub.
2. In the Cloudflare dashboard, go to Workers & Pages, create a Pages project, and connect it to the GitHub repository.
3. Use these build settings:
   - Framework preset: None
   - Build command: leave empty
   - Build output directory: `public`
4. Save and deploy. Every push to the main branch redeploys the site.

The page loads its fonts from Google Fonts and nothing else from outside.

## License

No license has been chosen yet. The underlying exhibits and GIS layers are the City of Petaluma's.
