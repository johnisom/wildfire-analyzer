import pygris
from .myutils import negativize_positive_longitudes
from pathlib import Path
import sqlite3
import pandas as pd
from threading import Lock
from shapely.geometry import Point

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
REGIONS_STATE_ALPHA_CODES['all'] = set(STATE_ALPHA_FIPS_CODES.keys())
DB_PATH = Path().parent / 'db' / 'fires.sqlite'

_counties_mutex = Lock()
_counties_geodf = None
def get_counties_geodf():
  global _counties_geodf
  global _counties_mutex
  with _counties_mutex:
    if _counties_geodf is None:
      _counties_geodf = pygris.counties(cb=True, year=2016)
      negativize_positive_longitudes(_counties_geodf)
  return _counties_geodf

_fips_codes_mutex = Lock()
_fips_codes_df = None
def get_fips_codes_dataframe():
  global _fips_codes_df
  global _fips_codes_mutex
  with _fips_codes_mutex:
    if _fips_codes_df is None:
      con = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
      _fips_codes_df = pd.read_sql_query('SELECT * FROM fips_codes', con)
      con.close()
  return _fips_codes_df

def get_state_fips_codes(keys):
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

def are_coordinates_inside_usa(lon, lat):
  counties_geodf = get_counties_geodf()
  possible_matches_indices = counties_geodf.sindex.intersection((lon, lat))
  possible_matches = counties_geodf.iloc[possible_matches_indices]
  exact_matches = possible_matches[possible_matches.intersects(Point(lon, lat))]
  return len(exact_matches) > 0
