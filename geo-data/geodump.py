import sqlite3
import json
import codecs

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

cur.execute('SELECT address, geodata FROM Locations')
fhand = codecs.open('where.js', 'w', 'utf-8')
fhand.write('myData = [\n')
count = 0
for row in cur:
    address = row[0]
    geodata = row[1]
    if not geodata:
        continue
    try:
        js = json.loads(geodata)
    except Exception:
        # skip invalid json
        continue

    if 'features' not in js or len(js['features']) == 0:
        continue

    try:
        feature = js['features'][0]
        coords = feature.get('geometry', {}).get('coordinates', [])
        if len(coords) < 2:
            continue
        lng = coords[0]
        lat = coords[1]
        where = feature.get('properties', {}).get('display_name', address)
        where = where.replace("'", "")
    except Exception as e:
        print('Unexpected format', e)
        continue

    print(where, lat, lng)

    count += 1
    if count > 1:
        fhand.write(',\n')
    output = '[' + str(lat) + ',' + str(lng) + ", '" + where + "']"
    fhand.write(output)

fhand.write('\n];\n')
cur.close()
fhand.close()
print(count, 'records written to where.js')
print('Open where.html to view the data in a browser')

