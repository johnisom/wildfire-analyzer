import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from state_and_county_info import get_state_fips_codes

def plot_counties_by_number_of_fires(counties_geo_df, keys, plot_title):
  fips_codes = get_state_fips_codes(keys)
  counties_geo_df = counties_geo_df[counties_geo_df['STATEFP'].isin(fips_codes)]
  zero_fire_counts = counties_geo_df[counties_geo_df.fire_count == 0]
  more_than_zero_fire_counts = counties_geo_df[counties_geo_df.fire_count > 0]
  fig, ax = plt.subplots(figsize=[12, 8])
  zero_fire_counts.plot(ax=ax, color='grey', legend=True)
  more_than_zero_fire_counts.plot(ax=ax, column='fire_count', legend=True, norm=LogNorm(vmin=more_than_zero_fire_counts.fire_count.min(), vmax=more_than_zero_fire_counts.fire_count.max()))
  ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
  ax.set_title(plot_title)
  fig.supxlabel('(Gray means zero fires were reported)')
  fig.tight_layout()
  plt.show()

def plot_counties_by_total_area_burned(counties_geo_df, keys, plot_title):
  fips_codes = get_state_fips_codes(keys)
  counties_geo_df = counties_geo_df[counties_geo_df['STATEFP'].isin(fips_codes)]
  zero_acres_burned = counties_geo_df[counties_geo_df.acres_burned == 0]
  more_than_zero_acres_burned = counties_geo_df[counties_geo_df.acres_burned > 0]
  fig, ax = plt.subplots(figsize=[12, 8])
  zero_acres_burned.plot(ax=ax, color='grey', legend=True)
  more_than_zero_acres_burned.plot(ax=ax, column='fire_count', legend=True, norm=LogNorm(vmin=more_than_zero_acres_burned.fire_count.min(), vmax=more_than_zero_acres_burned.fire_count.max()))
  ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
  ax.set_title(plot_title)
  fig.supxlabel('(Gray means zero fires were reported)')
  fig.tight_layout()
  plt.show()

def plot_causes_of_fires_by_state(fire_causes_dataframe, keys, plot_title):
  state_fips_codes = get_state_fips_codes(keys)
  relevant_df = fire_causes_dataframe[fire_causes_dataframe.state_fips_code.isin(state_fips_codes)]
  df = relevant_df.value_counts('stat_cause_descr')
  fig, ax = plt.subplots(figsize=[12, 8])
  df.plot.pie(ax=ax, title=plot_title, legend=True)
  fig.tight_layout()
  plt.show()
