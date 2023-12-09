def add_fire_count_to_counties(geoid_indexed_counties, con, min_year, max_year):
  sql = 'SELECT combined_fips_code, COUNT(id) FROM fires WHERE fire_year BETWEEN ? AND ? GROUP BY combined_fips_code'
  geoid_indexed_counties['fire_count'] = 0
  for fips_code, count in con.execute(sql, (min_year, max_year)).fetchall():
    geoid_indexed_counties.loc[fips_code, 'fire_count'] = count

def add_acres_burned_to_counties(geoid_indexed_counties, con, min_year, max_year):
  sql = 'SELECT combined_fips_code, SUM(fire_size) FROM fires WHERE fire_year BETWEEN ? AND ? GROUP BY combined_fips_code'
  geoid_indexed_counties['acres_burned'] = 0.0
  for fips_code, acres_burned in con.execute(sql, (min_year, max_year)).fetchall():
    geoid_indexed_counties.loc[fips_code, 'acres_burned'] = acres_burned

def get_min_max_fire_years(con):
  return con.execute('SELECT MIN(fire_year), MAX(fire_year) FROM fires').fetchone()
