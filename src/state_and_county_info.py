import pygris
from .myutils import negativize_positive_longitudes

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

_counties = None

def get_all_counties():
  global _counties
  if _counties is None:
    print('Loading data on all US counties...')
    _counties = pygris.counties(cb=True)
    negativize_positive_longitudes(_counties)
  return _counties

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
