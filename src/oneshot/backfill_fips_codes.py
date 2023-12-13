import sqlite3
from shapely.geometry import Point
from ..location_info import get_counties_geodf

DB_FILENAME = 'db/fires.sqlite'

def backfill_location_information(dryrun=False):
  print('loading counties')
  counties = get_counties_geodf()
  geoidx = counties.sindex
  print('connecting to db')
  con = sqlite3.connect(DB_FILENAME)
  cur = con.cursor()

  # build fires_coordinate_county_indices
  # looks like {(latitude,longitude):index_of_counties,...}
  print('loading longitude and latitude from db')
  fires_coordinate_county_indices = []
  for id, lon, lat in cur.execute('SELECT id, longitude, latitude FROM fires WHERE combined_fips_code IS NULL'):
    fires_coordinate_county_indices.append([id, (lon, lat), None])

  if len(fires_coordinate_county_indices) == 0:
    print('No records to update. exiting...')
    return

  # map full fips code to state name and county name
  print('loading fips_codes database table')
  fips_codes_to_state_county_name = {}
  for state_numeric_code, county_numeric_code, state_name, county_name in cur.execute('SELECT state_numeric_code, county_numeric_code, state_name, county_name FROM fips_codes'):
    fips_codes_to_state_county_name[state_numeric_code + county_numeric_code] = (state_name, county_name)

  # map the coordinates to the respective counties index
  print('mapping longitude and latitude to county')
  for elem in fires_coordinate_county_indices:
    lon, lat = elem[1]
    possible_matches_indices = geoidx.intersection((lon, lat))
    possible_matches = counties.iloc[possible_matches_indices]
    precise_matches = possible_matches[possible_matches.intersects(Point(lon, lat))]
    county_idx = precise_matches.iloc[0].name
    elem[2] = county_idx

  # now we can update the county fips codes to the database
  batch_size = 1000
  batch = []
  i = 1
  print('starting batch update now')
  for id, (_lon, _lat), counties_idx in fires_coordinate_county_indices:
    county = counties.iloc[counties_idx]
    county_fips_code = county['COUNTYFP']
    state_fips_code = county['STATEFP']
    county_fips_name = county['NAME']
    combined_fips_code = state_fips_code + county_fips_code
    state_name, county_name = fips_codes_to_state_county_name[combined_fips_code]
    batch.append((county_fips_code, state_fips_code, county_fips_name, combined_fips_code, state_name, county_name, id))
    i += 1
    if i % batch_size == 0:
      print(f'doing batch. i: {i - batch_size + 1}-{i}; id: {id - batch_size + 1}-{id}')
      cur.executemany('UPDATE fires SET county_fips_code = ?, state_fips_code = ?, county_fips_name = ?, combined_fips_code = ?, state_name = ?, county_name = ? WHERE id = ?', batch)
      batch = []
      if dryrun:
        con.rollback()
        print('rolled back')
      else:
        con.commit()
        print('commited')

  print(f'doing batch. i: -{i}; id: -{id}')
  cur.executemany('UPDATE fires SET county_fips_code = ?, state_fips_code = ?, county_fips_name = ?, combined_fips_code = ?, state_name = ?, county_name = ? WHERE id = ?', batch)
  batch = []
  if dryrun:
    con.rollback()
    print('rolled back')
  else:
    con.commit()
    print('commited')
  con.close()
