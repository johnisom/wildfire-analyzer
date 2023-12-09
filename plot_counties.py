import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import pygris
import sqlite3

STATE_ALPHA_FIPS_CODES = {
  'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08', 'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12', 'GA': '13', 'HI': '15', 'ID': '16',
  'IL': '17', 'IN': '18', 'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29',
  'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34', 'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42',
  'RI': '44', 'SC': '45', 'SD': '46', 'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55', 'WY': '56', 'PR': '72',
}
STATE_FIPS_ALPHA_CODES = { value: key for key, value in STATE_ALPHA_FIPS_CODES.items() }
REGIONS_STATE_ALPHA_CODES = {
  'west': { 'WA', 'OR', 'CA', 'NV', 'ID', 'UT', 'AZ', 'NM', 'CO', 'WY', 'MT' },
  'midwest': { 'ND', 'SD', 'NE', 'KS', 'IA', 'MN', 'IL', 'MO', 'WI', 'MI', 'IN', 'OH' },
  'south': { 'OK', 'TX', 'AR', 'LA', 'DE', 'MD', 'DC', 'VA', 'WV', 'NC', 'SC', 'GA', 'FL', 'AL', 'MS', 'TN', 'KY' },
  'northeast': { 'PA', 'NJ', 'NY', 'CT', 'RI', 'MA', 'VT', 'NH', 'ME' },
  'pacific': { 'AK', 'HI' },
}
REGIONS_STATE_ALPHA_CODES['lower48'] = { code for region in ('west', 'midwest', 'south', 'northeast') for code in REGIONS_STATE_ALPHA_CODES[region] }
ALPHA_CODE_COLORS = {
  'AK': 'blue', 'AL': 'green', 'AR': 'green', 'AZ': 'orange', 'CA': 'blue', 'CO': 'red', 'CT': 'blue', 'DC': 'yellow', 'DE': 'green',
  'FL': 'red', 'GA': 'blue', 'HI': 'red', 'IA': 'orange', 'ID': 'orange', 'IL': 'green', 'IN': 'red', 'KS': 'green', 'KY': 'blue',
  'LA': 'red', 'MA': 'red', 'MD': 'red', 'ME': 'green', 'MI': 'blue', 'MN': 'green', 'MO': 'red', 'MS': 'blue', 'MT': 'blue',
  'NC': 'red', 'ND': 'orange', 'NE': 'blue', 'NH': 'blue', 'NJ': 'red', 'NM': 'green', 'NV': 'green', 'NY': 'green', 'OH': 'green',
  'OK': 'orange', 'OR': 'red', 'PA': 'blue', 'PR': 'orange', 'RI': 'orange', 'SC': 'green', 'SD': 'red', 'TN': 'orange', 'TX': 'blue',
  'UT': 'blue', 'VA': 'green', 'VT': 'orange', 'WA': 'green', 'WI': 'red', 'WV': 'orange', 'WY': 'green'
}
COUNTIES = pygris.counties(year=2017, cb=True)

def joinand(iterable):
  if len(iterable) == 0:
    return ''
  if len(iterable) == 1:
    return iterable[0]
  return ' and '.join((', '.join(iterable[:-1]), iterable[-1]))

def add_fire_count_to_counties(geoid_indexed_counties, con):
  geoid_indexed_counties['fire_count'] = 0
  for fips_code, count in con.execute('SELECT combined_fips_code, COUNT(id) FROM fires GROUP BY combined_fips_code').fetchall():
    geoid_indexed_counties.loc[fips_code, 'fire_count'] = count

def add_acres_burned_to_counties(geoid_indexed_counties, con):
  geoid_indexed_counties['acres_burned'] = 0.0
  for fips_code, acres_burned in con.execute('SELECT combined_fips_code, SUM(fire_size) FROM fires GROUP BY combined_fips_code').fetchall():
    geoid_indexed_counties.loc[fips_code, 'acres_burned'] = acres_burned

def get_min_max_fire_years(con):
  return con.execute('SELECT MIN(fire_year), MAX(fire_year) FROM fires').fetchone()

def get_fips_codes(keys):
  fips_codes = set()
  if type(keys) != tuple:
    keys = (keys,)
  for key in keys:
    if key in STATE_ALPHA_FIPS_CODES:
      fips_codes.add(STATE_ALPHA_FIPS_CODES[key])
    elif key in REGIONS_STATE_ALPHA_CODES:
      for alpha_code in REGIONS_STATE_ALPHA_CODES[key]:
        fips_codes.add(STATE_ALPHA_FIPS_CODES[alpha_code])
    else:
      raise ValueError(f'key must be census region or 2-letter state code, instead got {key!r}')
  return fips_codes


def plot_counties_by_number_of_fires(counties, keys=('lower48',), plot_title='Number of reported wildfires in the US by county'):
  fips_codes = get_fips_codes(keys)
  counties = counties[counties['STATEFP'].isin(fips_codes)]
  zero_fire_counts = counties[counties.fire_count == 0]
  more_than_zero_fire_counts = counties[counties.fire_count > 0]
  fig, ax = plt.subplots(figsize=[12, 8])
  zero_fire_counts.plot(ax=ax, color='grey', legend=True)
  more_than_zero_fire_counts.plot(ax=ax, column='fire_count', legend=True, norm=LogNorm(vmin=more_than_zero_fire_counts.fire_count.min(), vmax=more_than_zero_fire_counts.fire_count.max()))
  ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
  ax.set_title(plot_title)
  fig.supxlabel('(Gray means zero fires were reported)')
  fig.tight_layout()
  plt.show()

def plot_counties_by_total_area_burned(counties, keys=('lower48',), plot_title='Number of reported acres burned by wildfires in the US by county'):
  fips_codes = get_fips_codes(keys)
  counties = counties[counties['STATEFP'].isin(fips_codes)]
  zero_acres_burned = counties[counties.acres_burned == 0]
  more_than_zero_acres_burned = counties[counties.acres_burned > 0]
  fig, ax = plt.subplots(figsize=[12, 8])
  zero_acres_burned.plot(ax=ax, color='grey', legend=True)
  more_than_zero_acres_burned.plot(ax=ax, column='fire_count', legend=True, norm=LogNorm(vmin=more_than_zero_acres_burned.fire_count.min(), vmax=more_than_zero_acres_burned.fire_count.max()))
  ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
  ax.set_title(plot_title)
  fig.supxlabel('(Gray means zero fires were reported)')
  fig.tight_layout()
  plt.show()

con = sqlite3.connect('db/fires.sqlite')
counties = COUNTIES.set_index('GEOID')
add_fire_count_to_counties(counties, con)
add_acres_burned_to_counties(counties, con)
min_year, max_year = get_min_max_fire_years(con)
plot_title = f'Number of reported wildfires in the US by county between {min_year} and {max_year}'
plot_counties_by_number_of_fires(counties, 'lower48', plot_title=plot_title)
plot_title = f'Number of reported acres burned by wildfires in the US by county between {min_year} and {max_year}'
plot_counties_by_total_area_burned(counties, 'lower48', plot_title=plot_title)

con.close()