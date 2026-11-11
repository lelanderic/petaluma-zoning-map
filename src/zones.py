# Zone facts transcribed from Exhibit B (Amendments in Clean, Nov 9 2026).
GROUPS = [
    ("res", "Residential", "#E9B824"),
    ("mu", "Mixed use", "#8A5BB0"),
    ("ci", "Commercial & industrial", "#D8604C"),
    ("civ", "Civic & schools", "#3F86B8"),
    ("park", "Parks & open space", "#4E9E55"),
    ("fw", "Floodway", "#3212F2"),
    ("pd", "Planned districts", "#C9B38C"),
]

ZO = "Zoning Ordinance"
SC = "SmartCode (Central Petaluma Specific Plan)"


def res(code, name, s, gp, was, dens, lot, ht, far, types, n):
    std = [["Homes per net acre", dens], ["Height limit", ht], ["Minimum lot", lot], ["Housing types", types]]
    if far:
        std.insert(2, ["Floor area ratio", far])
    return dict(c=code, n=name, g="res", s=s, gp=gp, was=was, by=ZO, std=std,
                ref=f"Purpose §4.020(A)({n}) · Uses Table 4.1 · Standards Table 4.5")


def mu(code, name, s, gp, was, dens, far, ht, n, extra=None):
    std = [["Homes per net acre", dens], ["Height limit", ht], ["Floor area ratio", far]]
    if extra:
        std.append(extra)
    return dict(c=code, n=name, g="mu", s=s, gp=gp, was=was, by=ZO, std=std,
                ref=f"Purpose §4.020(B)({n}) · Uses Table 4.2 · Standards Table 4.6")


def ci(code, name, s, gp, was, far, ht, lot, n, uses="Uses Table 4.3"):
    std = [["Height limit", ht], ["Floor area ratio", far], ["Minimum lot", lot]]
    return dict(c=code, n=name, g="ci", s=s, gp=gp, was=was, by=ZO, std=std,
                ref=f"Purpose §4.020(C)({n}) · {uses} · Standards Table 4.7")


def pub(code, name, g, s, gp, was, ht, lot, n):
    std = [["Height limit", ht], ["Lot size and setbacks", lot]]
    return dict(c=code, n=name, g=g, s=s, gp=gp, was=was, by=ZO, std=std,
                ref=f"Purpose §4.020(D)({n}) · Uses Table 4.4 · Standards Table 4.8")


def sc(code, name, g, s, gp, was, col, urban, note=None):
    std = [["Allowed uses", f"SmartCode Table 3.1, {col} column"], ["Building standards", urban],
           ["Also applies", "Standards the General Plan assigns to this designation (SmartCode §2.50)"]]
    d = dict(c=code, n=name, g=g, s=s, gp=gp, was=was, by=SC, std=std,
             ref="SmartCode §2.30 and §2.40 (Exhibit B, SmartCode Section 2)")
    if note:
        d["note"] = note
    return d


ZONES = [
    res("R-VLR", "Very Low Density Residential", "Single-family homes on larger lots, mostly on the western hillsides.",
        "Very Low Density Residential (VLR)", "R1", "0.6 – 2.5", "20,000 sq ft", "25 ft (2 stories)", None,
        "Single-family, plex, townhouse", 2),
    res("R-RLD", "Low Density Residential", "Established single-family neighborhoods with room for infill.",
        "Low Density Residential (RLD)", "R2", "2.6 – 12", "2,800 sq ft", "25 ft (2 stories)", None,
        "Single-family, plex, townhouse", 3),
    res("R-RDIV", "Diverse Low Density Residential",
        "Older neighborhoods in and near downtown with a walkable mix of housing types.",
        "Diverse Low Density Residential (RDIV)", "R3", "6.1 – 15", "2,800 sq ft", "25 ft (2 stories)",
        "1.0 for 3–7 units; 1.25 for 8–10 units", "Single-family, multifamily, plex, townhouse", 4),
    res("R-RMD", "Medium Density Residential", "Attached homes, plexes and apartments.",
        "Medium Density Residential (RMD)", "R4", "12 – 22", "2,800 sq ft", "35 ft (3 stories)", "1.5",
        "Multifamily, plex, townhouse", 5),
    res("R-RHD", "High Density Residential", "The most urban housing types and higher-density apartments.",
        "High Density Residential (RHD)", "R5", "22.1 – 45", "1,500 sq ft", "45 ft (4 stories)", "2.25",
        "Multifamily, plex, townhouse", 6),
    dict(c="R-MH", n="Mobile Homes", g="res", s="Existing mobile home parks.", gp="Mobile Homes (MH)", was="MH", by=ZO,
         std=[["Allowed", "Mobile home park with its usual accessory facilities, such as a manager's residence, community building and recreation facilities"],
              ["Standards", "Not in the Chapter 4 tables; see §4.030(C)"]],
         ref="Purpose §4.020(A)(7) · Uses and standards §4.030(C)"),
    mu("MU-MC", "Mini-Center Mixed Use",
       "Smaller sites in and next to single-family neighborhoods, for homes, businesses or both at neighborhood scale.",
       "Mini-Center Mixed Use (MC-MU)", "MU1C", "12 – 30", "2.0", "40 ft (3 stories)", 1,
       ["Step-down", "30 ft (2 stories) within 25 ft of rear and side property lines"]),
    mu("MU-NC", "Neighborhood Center Mixed Use",
       "Small neighborhood centers and gathering places with local shops and services, along corridors and on larger arterial sites.",
       "Neighborhood Center Mixed Use (NC-MU)", "MU1A, MU1B", "15 – 30", "2.0", "40 ft (3 stories)", 2),
    mu("MU-SD", "Stepdown Mixed Use",
       "Near-downtown areas with a downtown-like mix, where building height steps down next to residential neighborhoods.",
       "Stepdown Mixed Use (SD-MU)", "MU2 (part)", "20 – 45", "2.5", "50 ft (4 stories)", 3,
       ["Step-down", "35 ft (3 stories) within 35 ft of a lower-height residential zone, or a 45 ft setback"]),
    mu("MU-DT", "Downtown Mixed Use",
       "The historic downtown and adjacent blocks: active ground floors with homes or other uses above.",
       "Downtown Mixed Use (DT-MU)", "MU2 (part)", "0 – 45 (no minimum)", "4.0", "45 ft (4 stories)", 4,
       ["All-residential projects", "Only on lots shown on the Downtown 100% Residential Opportunities Map (§4.060)"]),
    mu("MU-UC", "Urban Corridor Mixed Use",
       "Corridor sites for higher-intensity development with active ground floors and pedestrian frontages.",
       "Urban Corridor Mixed Use (UC-MU)", "MU2 (part)", "30 – 75", "3.5", "60 ft (5 stories)", 6,
       ["Step-down", "50 ft (4 stories) within 15 ft of a property line abutting a residential zone"]),
    ci("CI-NC", "Neighborhood Commercial", "Small clusters of local shops and services that serve the surrounding neighborhood.",
       "Neighborhood Commercial (NC)", "C1", "0.8 (non-residential floor area)", "30 ft (2 stories)", "None", 1),
    ci("CI-CC", "Community Commercial", "Existing community and regional shopping centers and commercial areas.",
       "Community Commercial (CC)", "C2", "1.2 (non-residential floor area)", "40 ft (3 stories)", "None", 2),
    ci("CI-BP", "Business Park",
       "Offices, technology parks, research and development, light industrial and visitor services, with retail secondary.",
       "Business Park (BP)", "BP (part)", "1.5; up to 2.0 to fit above-grade structured parking", "50 ft (3 stories)", "20,000 sq ft", 3),
    ci("CI-MKR", "Maker and Microbusiness",
       "Small-scale production, artisan manufacturing, food and beverage production and most other non-residential uses short of heavy industry.",
       "Maker/Microbusiness (M/M)", None, "1.5; up to 2.0 to fit above-grade structured parking", "50 ft (3 stories)", "20,000 sq ft", 4,
       uses="Uses Chapter 29"),
    ci("CI-IND", "Industrial",
       "Manufacturing, industrial and food processing, general services, warehousing, storage and distribution.",
       "Industrial (I)", "I", "0.6", "40 ft (2 stories)", "20,000 sq ft", 5),
    ci("CI-AG", "Agriculture", "Land actively used for grazing or for producing or selling food and fiber.",
       "Agriculture (AG)", "AG", "Not applicable", "25 ft (2 stories)", "20,000 sq ft", 6),
    pub("P-PSP", "Public/Semi-Public Space", "civ",
        "Civic and government offices, public utilities and community uses such as houses of worship.",
        "Public/Semi-Public (PSP)", "CF (part)", "35 ft (3 stories)", "Same as the abutting zone", 1),
    pub("P-ED", "Education", "civ",
        "Land of school and community college districts, and private and parochial schools. Not preschools.",
        "Education (ED)", "CF (part)", "35 ft (3 stories)", "Same as the abutting zone", 2),
    pub("P-PK", "Parks", "park", "City-owned and private land whose main purpose is recreation.",
        "Parks (P)", "OSP (part)", "25 ft (2 stories)", "Same as the abutting zone", 3),
    pub("P-OS", "Open Space", "park",
        "Unimproved land kept for natural and cultural resources, outdoor recreation or public safety.",
        "Open Space (OS)", "OSP (part)", "25 ft (2 stories)", "No minimum lot; 40 ft front, rear and street-side setbacks, 20 ft interior side", 4),
    pub("P-US", "Urban Separator", "park",
        "Open land at the Urban Growth Boundary that buffers the city from agricultural land.",
        "Urban Separator (US)", "OSP (part)", "Not applicable", "No minimum lot; 40 ft front, rear and street-side setbacks, 20 ft interior side", 5),
    dict(c="P-FW", n="Floodway", g="fw",
         s="Land mapped as Floodway on FEMA's Flood Insurance Rate Map. New construction, fill and more intensive uses are not allowed except as Chapter 6 provides.",
         gp="Floodway (FW)", was="FW", by=ZO,
         std=[["Uses and standards", "Chapter 6, §6.120"], ["Standards tables", "Not in the Chapter 4 tables"]],
         ref="Purpose §4.020(D)(6) · Uses and standards Chapter 6"),
    dict(c="PUD", n="Planned Unit District", g="pd",
         s="A planned development with its own adopted standards. What applies here depends on that district's approval documents. The General Plan land use underneath varies from place to place; hover or click to see it.",
         gp="As shown for the site on the General Plan Land Use Map", was=None, by=ZO,
         std=[["Standards", "Those adopted for the individual district, plus Chapter 19"], ["Allowed uses", "§4.030(D)"]],
         ref="§4.020(E) · §4.030(D) · Chapter 19"),
    dict(c="PCD", n="Planned Community District", g="pd",
         s="A planned community with its own adopted standards. No wholly new planned community districts may be created. The General Plan land use underneath varies from place to place; hover or click to see it.",
         gp="As shown for the site on the General Plan Land Use Map", was=None, by=ZO,
         std=[["Standards", "Those adopted for the individual district, plus Chapter 19"], ["Allowed uses", "§4.030(D)"]],
         ref="§4.020(E) · §4.030(D) · Chapter 19"),
    sc("T4-NC", "T4 Neighborhood Center", "mu", "Neighborhood center mixed use inside the Central Petaluma Specific Plan area.",
       "Neighborhood Center Mixed Use (NC-MU)", "T4", "T4", "SmartCode Table 4.10, T4"),
    sc("T5-TC", "T5 Town Center Mixed Use", "mu", "Town center mixed use inside the Central Petaluma Specific Plan area. Single-family dwellings are not allowed.",
       "Town Center Mixed Use (TC-MU)", "T5", "T5", "SmartCode Table 4.10, T5"),
    sc("T6-UC", "T6 Urban Corridor Mixed Use", "mu", "Urban corridor mixed use inside the Central Petaluma Specific Plan area.",
       "Urban Corridor Mixed Use (UC-MU)", "T6 (part)", "T6", "SmartCode Table 4.10, T6"),
    sc("T6-CORE", "T6 Urban Core Mixed Use", "mu", "Urban core mixed use inside the Central Petaluma Specific Plan area.",
       "Urban Core Mixed Use (CORE-MU)", "T6 (part)", "T6", "SmartCode Table 4.10, T6"),
    sc("T6-ST", "T6 Station Mixed Use", "mu", "Station-area mixed use inside the Central Petaluma Specific Plan area.",
       "Station Mixed Use (ST-MU)", "T6 (part)", "T6", "SmartCode Table 4.10, T6",
       note="A new zone: it is created by the SmartCode amendment that accompanies this ordinance (Table 2-1, note 10)."),
    sc("D1-AGS", "D1 Agricultural Support Industry", "ci", "Agricultural support industry district inside the Central Petaluma Specific Plan area.",
       "Agricultural Support Industry (AGS)", "D1", "D1", "SmartCode §4.20(A)"),
    sc("D2-RAIL", "D2 Railroad District", "ci", "Railroad district inside the Central Petaluma Specific Plan area.",
       "Railroad District (RAIL)", "D2", "D2", "SmartCode §4.20(B)",
       note="The General Plan assigns this designation no density, floor area ratio or height limit, so SmartCode §4.20(B) governs."),
    sc("D3-RDI", "D3 River-Dependent Industrial", "ci", "River-dependent industrial district inside the Central Petaluma Specific Plan area.",
       "River-Dependent Industrial District (RDI)", "D3", "D3", "SmartCode §4.20(C)"),
    sc("D4-TD", "D4 Thoroughfare", "ci", "Thoroughfare district inside the Central Petaluma Specific Plan area.",
       "Thoroughfare District (TD)", "D4", "D4", "SmartCode §4.20(D)"),
    dict(c="CS-PK", n="CS Parks", g="park", s="Park land inside the Central Petaluma Specific Plan area.",
         gp="Parks (P)", was="CS (part)", by=SC,
         std=[["Allowed uses", "Same as the P-PK zone (Zoning Ordinance Table 4.4)"],
              ["Building standards", "SmartCode urban standards do not apply; General Plan designation standards do"]],
         ref="SmartCode §2.40(B) (Exhibit B, SmartCode Section 2)"),
    dict(c="CS-PSP", n="CS Public/Semi-Public Space", g="civ", s="Public and semi-public land inside the Central Petaluma Specific Plan area.",
         gp="Public/Semi-Public (PSP)", was="CS (part)", by=SC,
         std=[["Allowed uses", "Same as the P-PSP zone (Zoning Ordinance Table 4.4)"],
              ["Building standards", "SmartCode urban standards do not apply; General Plan designation standards do"]],
         ref="SmartCode §2.40(B) (Exhibit B, SmartCode Section 2)"),
    dict(c="CS-FW", n="Floodway (Central Petaluma)", g="fw",
         s="Floodway inside the Central Petaluma Specific Plan area. Regulated the same as P-FW.",
         gp="Floodway (FW)", was="CS (part)", by=ZO,
         std=[["Uses and standards", "Zoning Ordinance Chapters 4 and 6; SmartCode standards do not apply"]],
         note="The map legend labels this CS-FW. The ordinance text says the SmartCode establishes no floodway zone and that this land is zoned P-FW (Table 2-1, note 6; SmartCode §2.30(D)).",
         ref="Table 2-1 note 6 · SmartCode §2.30(D) · Chapter 6"),
]

OVERLAYS = [
    dict(k="fp100", n="Flood plain: FEMA 100-year", short="100-year floodplain", col="#3D6FD6",
         d="Flood Plain/Flood Prone Area overlay (-FP). Chapter 6 applies in addition to the base zone."),
    dict(k="fp500", n="Flood plain: FEMA 500-year", short="500-year floodplain", col="#1FA890",
         d="Flood Plain/Flood Prone Area overlay (-FP). Chapter 6 applies in addition to the base zone."),
    dict(k="hist", n="Historic district", short="Historic District overlay", col="#00226E",
         d="Historic District overlay (-H). See Chapter 15 and the district's guidelines."),
    dict(k="smh", n="Senior mobile home park", short="Senior Mobile Home Park overlay", col="#8A5A12",
         d="Senior Mobile Home Park overlay (-SMH), §5.060."),
    dict(k="fair", n="Fairgrounds", short="Fairgrounds overlay", col="#2A7A0A",
         d="Fairgrounds overlay (-FG), §5.080."),
    dict(k="t6o", n="T6-Open", short="T6-O Urban Core – Open overlay", col="#111111",
         d="T6-O overlay within T6-ST: allows additional ground-floor uses (SmartCode §2.30(E))."),
]

# Street labels: positions and angles computed from the City's public GIS street centerlines (gis/labels.py).
import json as _json
LABELS = _json.loads(r'''[{"t": "E Washington St", "x": 1696, "y": 1319, "a": -51.9, "lvl": 1}, {"t": "E Washington St", "x": 1924, "y": 1007, "a": -54.2, "lvl": 0}, {"t": "N McDowell Blvd", "x": 1337, "y": 751, "a": 35.9, "lvl": 0}, {"t": "S McDowell Blvd", "x": 2149, "y": 1341, "a": 36.0, "lvl": 1}, {"t": "Sonoma Mountain Pkwy", "x": 1723, "y": 677, "a": 35.9, "lvl": 1}, {"t": "Ely Blvd S", "x": 2329, "y": 1119, "a": 36.0, "lvl": 0}, {"t": "Lakeville Hwy", "x": 2530, "y": 1591, "a": -6.1, "lvl": 0}, {"t": "Petaluma Blvd N", "x": 1384, "y": 1285, "a": 77.5, "lvl": 0}, {"t": "Petaluma Blvd N", "x": 1016, "y": 789, "a": 26.8, "lvl": 2}, {"t": "Petaluma Blvd S", "x": 1677, "y": 1695, "a": 26.4, "lvl": 1}, {"t": "D St", "x": 1484, "y": 1808, "a": -63.6, "lvl": 1}, {"t": "Western Ave", "x": 1287, "y": 1670, "a": -21.9, "lvl": 2}, {"t": "Bodega Ave", "x": 1164, "y": 1576, "a": 2.6, "lvl": 2}, {"t": "Lakeville St", "x": 1664, "y": 1516, "a": 32.6, "lvl": 2}, {"t": "Payran St", "x": 1775, "y": 1414, "a": 35.7, "lvl": 2}, {"t": "Casa Grande Rd", "x": 2491, "y": 1429, "a": -54.3, "lvl": 2}, {"t": "Frates Rd", "x": 2655, "y": 1543, "a": -52.7, "lvl": 2}, {"t": "Old Redwood Hwy", "x": 783, "y": 262, "a": -80.2, "lvl": 2}, {"t": "Caulfield Ln", "x": 2146, "y": 1256, "a": -53.0, "lvl": 2}, {"t": "Corona Rd", "x": 1190, "y": 428, "a": -57.0, "lvl": 2}, {"t": "Rainier Ave", "x": 1670, "y": 832, "a": -48.7, "lvl": 2}, {"t": "Magnolia Ave", "x": 1200, "y": 1239, "a": 11.4, "lvl": 2}, {"t": "101", "x": 1097, "y": 690, "kind": "shield", "lvl": 1}, {"t": "101", "x": 1508, "y": 987, "kind": "shield", "lvl": 0}, {"t": "101", "x": 1957, "y": 1415, "kind": "shield", "lvl": 0}, {"t": "101", "x": 646, "y": 284, "kind": "shield", "lvl": 1}, {"t": "Petaluma River", "x": 2780, "y": 2215, "a": 42, "kind": "water", "lvl": 0}, {"t": "Downtown", "x": 1405, "y": 1612, "kind": "place", "lvl": 1}, {"t": "Fairgrounds", "x": 1800, "y": 1345, "kind": "place", "lvl": 2}, {"t": "0", "x": 560, "y": 2392, "kind": "scale", "lvl": 0}, {"t": "1 mile", "x": 1013, "y": 2392, "kind": "scale", "lvl": 0}, {"t": "N", "x": 500, "y": 2400, "kind": "north", "lvl": 0}]''')
