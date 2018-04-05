import sqlite3
import json

conn = None
ROCK_GRADES = ['3rd', '4th', 'Easy', '5th', '5.0', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.7+', '5.8-', '5.8', '5.8+', '5.9-', '5.9', '5.9+', '5.10a', '5.10-', '5.10a/b', '5.10b', '5.10', '5.10b/c', '5.10c', '5.10+', '5.10c/d', '5.10d', '5.11a', '5.11-', '5.11a/b', '5.11b', '5.11', '5.11b/c', '5.11c', '5.11+', '5.11c/d', '5.11d', '5.12a', '5.12-', '5.12a/b', '5.12b', '5.12', '5.12b/c', '5.12c', '5.12+', '5.12c/d', '5.12d', '5.13a', '5.13-', '5.13a/b', '5.13b', '5.13', '5.13b/c', '5.13c', '5.13+', '5.13c/d', '5.13d', '5.14a', '5.14-', '5.14a/b', '5.14b', '5.14', '5.14b/c', '5.14c', '5.14+', '5.14c/d', '5.14d', '5.15a', '5.15-', '5.15a/b', '5.15b', '5.15', '5.15c', '5.15+', '5.15c/d', '5.15d']
BOULDER_GRADES = ['V-easy', 'V0-', 'V0', 'V0+', 'V0-1', 'V1-', 'V1', 'V1+', 'V1-2', 'V2-', 'V2', 'V2+', 'V2-3', 'V3-', 'V3', 'V3+', 'V3-4', 'V4-', 'V4', 'V4+', 'V4-5', 'V5-', 'V5', 'V5+', 'V5-6', 'V6-', 'V6', 'V6+', 'V6-7', 'V7-', 'V7', 'V7+', 'V7-8', 'V8-', 'V8', 'V8+', 'V8-9', 'V9-', 'V9', 'V9+', 'V9-10', 'V10-', 'V10', 'V10+', 'V10-11', 'V11-', 'V11', 'V11+', 'V11-12', 'V12-', 'V12', 'V12+', 'V12-13', 'V13-', 'V13', 'V13+', 'V13-14', 'V14-', 'V14', 'V14+', 'V14-15', 'V15-', 'V15', 'V15+', 'V15-16', 'V16-', 'V16', 'V16+', 'V16-17', 'V17-', 'V17']
ICE_GRADES = ['WI1', 'AI1', 'AI1-2', 'WI2-', 'WI2', 'AI2', 'WI2+', 'WI2-3', 'AI2-3', 'WI3-', 'WI3', 'AI3', 'WI3+', 'WI3-4', 'AI3-4', 'WI4-', 'WI4', 'AI4', 'WI4+', 'WI4-5', 'AI4-5', 'WI5-', 'WI5', 'AI5', 'WI5+', 'WI5-6', 'AI5-6', 'WI6-', 'WI6', 'AI6', 'WI6+', 'WI6-7', 'WI7-', 'WI7', 'WI7+', 'WI7-8', 'WI8-', 'WI8']
AID_GRADES = ['C0', 'A0', 'C0+', 'A0+', 'C0-1', 'A0-1', 'C1-', 'A1-', 'C1', 'A1', 'C1+', 'A1+', 'C1-2', 'A1-2', 'C2-', 'A2-', 'C2', 'A2', 'C2+', 'A2+', 'C2-3', 'A2-3', 'C3-', 'A3-', 'C3', 'A3', 'C3+', 'A3+', 'C3-4', 'A3-4', 'C4-', 'A4-', 'C4', 'A4', 'C4+', 'A4+', 'C4-5', 'A4-5', 'C5-', 'A5-', 'C5', 'A5', 'C5+', 'A5+']
MIXED_GRADES = ['M1', 'M1+', 'M1-2', 'M2-', 'M2', 'M2+', 'M2-3', 'M3-', 'M3', 'M3+', 'M3-4', 'M4-', 'M4', 'M4+', 'M4-5', 'M5-', 'M5', 'M5+', 'M5-6', 'M6-', 'M6', 'M6+', 'M6-7', 'M7-', 'M7', 'M7+', 'M7-8', 'M8-', 'M8', 'M8+', 'M8-9', 'M9-', 'M9', 'M9+', 'M9-10', 'M10-', 'M10', 'M10+', 'M10-11', 'M11-', 'M11', 'M11+', 'M12-', 'M12', 'M12+', 'M13-', 'M13', 'M13+']
SNOW_GRADES = ['Easy Snow', 'Mod. Snow', 'Steep Snow', '', '']
SAFTEY_GRADES = ['G', 'PG13', 'R', 'X']
ROUTE_TYPES = ['Trad', 'Ice', 'Sport', 'TR', 'Alpine', 'Snow', 'Mixed', 'Aid', 'Boulder', 'Other']

def setup_database():
    global conn
    conn = sqlite3.connect("routes.db")

def close_database():
    global conn
    conn.close()

def try_add_column(name, typ):
    try:
        conn.cursor().execute('ALTER TABLE routes ADD COLUMN %s %s' % (name, typ))
        conn.commit()
    except:
        pass # handle the error

def add_columns():
    try_add_column("saftey", "DOUBLE")
    try_add_column("difficulty", "DOUBLE")
    try_add_column("pitches", "INTEGER")
    try_add_column("starVotes", "INTEGER")
    try_add_column("stars", "DOUBLE")
    try_add_column("latitude", "DOUBLE")
    try_add_column("longitude", "DOUBLE")
    try_add_column("name", "VARCHAR(255)")
    for typ in ROUTE_TYPES:
        try_add_column(typ, "INTEGER")

def get_pitches(pitches):
    if pitches == "":
        return 0
    return int(pitches)

def get_stars(stars):
    if stars == "":
        return 0
    return float(stars)

def get_difficulty(rating):
    if rating in ROCK_GRADES:
        return float(ROCK_GRADES.index(rating) / len(ROCK_GRADES))
    elif rating in BOULDER_GRADES:
        return float(BOULDER_GRADES.index(rating) / len(BOULDER_GRADES))
    elif rating in ICE_GRADES:
        return float(ICE_GRADES.index(rating) / len(ICE_GRADES))
    elif rating in AID_GRADES:
        return float(AID_GRADES.index(rating) / len(AID_GRADES))
    elif rating in MIXED_GRADES:
        return float(MIXED_GRADES.index(rating) / len(MIXED_GRADES))
    elif rating in SNOW_GRADES:
        return float(SNOW_GRADES.index(rating) / len(SNOW_GRADES))
    else:
        return 0

def get_grade(rating):
    ratings = rating.split()
    saftey = 0
    difficulty = 0
    if ratings[-1] in SAFTEY_GRADES:
        saftey = float(SAFTEY_GRADES.index(ratings[-1]) / len(SAFTEY_GRADES))
        del ratings[-1]
    if 'Snow' in ratings:
        index = ratings.index('Snow')
        ratings[index - 1] += ' Snow'
        del ratings[index]
    for r in ratings:
        difficulty = max(difficulty, get_difficulty(r))
    return saftey, difficulty

def get_types(types):
    types = types.split(",")
    types = [t.strip() for t in types]
    trad = 1 if "Trad" in types else 0
    ice = 1 if "Ice" in types else 0
    sport = 1 if "Sport" in types else 0
    tr = 1 if "TR" in types else 0
    alpine = 1 if "Alpine" in types else 0
    snow = 1 if "Snow" in types else 0
    mixed = 1 if "Mixed" in types else 0
    aid = 1 if "Aid" in types else 0
    boulder = 1 if "Boulder" in types else 0
    other = 1 if "Other" in types else 0
    return trad, ice, sport, tr, alpine, snow, mixed, aid, boulder, other

def parse_json(id, json):
    pitches = get_pitches(json["pitches"])
    name = json["name"]
    lat = float(json["latitude"])
    lon = float(json["longitude"])
    stars = get_stars(json["stars"])
    starVotes = int(json["starVotes"])
    saftey, difficulty = get_grade(json["rating"])
    trad, ice, sport, tr, alpine, snow, mixed, aid, boulder, other = get_types(json["type"])
    conn.cursor().execute('UPDATE routes SET pitches = ?,' +
                            'name = ?, ' +
                            'latitude = ?, longitude = ?, stars = ?, starVotes = ?, ' +
                            'saftey = ?, difficulty = ?, Trad = ?, Ice = ?, ' +
                            'Sport = ?, TR = ?, Alpine = ?, Snow = ?, Mixed = ?, ' +
                            'Aid = ?, Boulder = ?, Other = ? ' +
                            'WHERE mountain_project_id = ?', (pitches, name, lat, lon, stars, starVotes, saftey, difficulty, trad, ice, sport, tr, alpine, snow, mixed, aid, boulder, other, id))
    conn.commit()

def parse_apis():
    cur = conn.cursor()
    cur.execute('SELECT mountain_project_id, api FROM routes WHERE saftey IS NULL')
    while True:
        result = cur.fetchone()
        if not result:
            exit()
        else:
             id, json_string = result
             if json_string is not None:
                 parse_json(id, json.loads(json_string))

setup_database()
add_columns()
parse_apis()
close_database()
