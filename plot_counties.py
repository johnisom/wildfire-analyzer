import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import sqlite3
from myutils import add_fire_count_to_counties, add_acres_burned_to_counties, get_min_max_fire_years
from state_and_county_info import COUNTIES, get_state_fips_codes

def plot_counties_by_number_of_fires(counties, keys, plot_title):
  fips_codes = get_state_fips_codes(keys)
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

def plot_counties_by_total_area_burned(counties, keys, plot_title):
  fips_codes = get_state_fips_codes(keys)
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
min_year, max_year = get_min_max_fire_years(con)
counties = COUNTIES.set_index('GEOID')
add_fire_count_to_counties(counties, con, min_year, max_year)
add_acres_burned_to_counties(counties, con, min_year, max_year)
plot_title = f'Number of reported wildfires in the US by county between {min_year} and {max_year}'
plot_counties_by_number_of_fires(counties, 'lower48', plot_title)
plot_title = f'Number of reported acres burned by wildfires in the US by county between {min_year} and {max_year}'
plot_counties_by_total_area_burned(counties, 'lower48', plot_title)

con.close()
