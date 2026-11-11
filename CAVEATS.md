# Caveats

Read this before relying on the map or sharing it.

## Status

- **Unofficial.** This is not a City of Petaluma product. It is a reading aid built from public City documents.
- **Draft zoning.** It shows the proposed citywide zoning map (Exhibit C) and ordinance amendments (Exhibit B), both dated November 9, 2026. Neither had been adopted when this was built, and either may change.
- **Not for property decisions.** For anything that matters about a specific property, confirm with the City of Petaluma Planning Division.

## How zones are determined

- **Zones are read from the colors of the Exhibit C map image, not from parcel records.** The City had not published a GIS layer of the proposed zoning when this was built.
- **Edges and small parcels can be wrong.** One map pixel is about 12 feet. Along zone boundaries and on very small parcels, the zone shown can be off by a few pixels.
- **Interior accuracy check.** Away from zone edges, the zone read from the map agrees with the City's parcel-level General Plan 2050 land use layer on 99.5% of land, with no sizeable area of disagreement. This checks the color reading. It does not check the City's map.
- **Streets are not zoned on this map.** Pointing at a street shows the nearest zone within about 70 feet.
- **Planned districts.** PUD and PCD areas have their own adopted standards, which this map does not include.

## Zone descriptions and standards

- **Paraphrased.** The one-line descriptions are short paraphrases of the purpose statements in Exhibit B §4.020 and SmartCode Section 2.
- **Simplified.** Density, height, floor area ratio and lot size come from Exhibit B Tables 4.5 to 4.8. Table footnotes, exceptions, step-down details and bonus provisions are mostly left out. Allowed uses are not listed.
- **Central Petaluma Specific Plan zones** (T4, T5, T6, D1 to D4, CS) are regulated by the SmartCode. The map points to the relevant SmartCode table or section and does not summarize those standards.
- **"Formerly" zone names** come from Exhibit B Table 2-2. Where one former zone splits into several new ones, the map says "(part)".

## Overlays

- **Traced from the image.** Flood plain, historic district, senior mobile home park, fairgrounds and T6-Open areas are traced from the overlay page of Exhibit C. Boundaries are approximate.
- **Flood plain.** The 100-year and 500-year areas are filled in from hatch patterns on the map, which blurs their edges. Use FEMA's maps for flood questions.
- **Senior mobile home parks.** Four areas were traced. Exhibit B §5.060 refers to five parks. Two adjacent parks may have merged in the tracing, or one may be missing.
- **Historic districts.** Very small districts or individual sites may not have been picked up.

## Data from the City's public GIS

Downloaded November 10, 2026 from `maps.cityofpetaluma.net`. These layers can change after that date.

- **General Plan land use** comes from the adopted General Plan 2050 parcel layer. It is laid under zone boundaries that still come from the map image, so at an edge the map can pair a zone with its neighbor's designation.
- **PUD and PCD names** come from the City's current zoning layer, which reflects the 2008 ordinance. They cover about 95% of the proposed PUD and PCD land. Names are missing on the rest and may be out of date where districts have changed.
- **Street names and label positions** come from the City's street centerline layer, fitted to the map image. Label positions and the scale bar are approximate.

## Things in the source documents worth knowing

- **Floodway label.** The map legend labels floodway inside the Central Petaluma Specific Plan area as "CS-FW". Exhibit B says the SmartCode establishes no floodway zone and that this land is zoned P-FW (Table 2-1 note 6; SmartCode §2.30(D)). The map follows the legend's label and notes the discrepancy.
- **Zones not on the map legend.** Exhibit B establishes R-RR (Rural Residential) and MU-TC (Town Center Mixed Use), which do not appear in the Exhibit C legend. This map therefore has no areas with those zones.

## Choices made by this map

- **"7 simple groups"** is this map's own grouping for readability. It is not a classification in the ordinance. In particular, the SmartCode T zones are grouped with mixed use and the D zones with commercial and industrial.
- **"Share of map"** figures are estimates from pixel counts and leave out streets.

## How it was made

The map was built with Claude, an AI model, from the two exhibits and the City's public GIS layers. Zone facts were transcribed from Exhibit B and spot-checked, but they have not been reviewed by City staff or a planner.
