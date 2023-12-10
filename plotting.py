import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from state_and_county_info import get_state_fips_codes

def plot_counties_by_number_of_fires(counties_geo_df, keys, plot_title):
  fips_codes = get_state_fips_codes(keys)
  counties_geo_df = counties_geo_df[counties_geo_df['STATEFP'].isin(fips_codes)]
  zero_fire_counts = counties_geo_df[counties_geo_df.fire_count == 0]
  more_than_zero_fire_counts = counties_geo_df[counties_geo_df.fire_count > 0]
  fig, ax = plt.subplots(figsize=[12, 8])
  zero_fire_counts.plot(ax=ax, color='grey', legend=True, aspect=1)
  more_than_zero_fire_counts.plot(ax=ax, column='fire_count', legend=True, norm=LogNorm(vmin=more_than_zero_fire_counts.fire_count.min(), vmax=more_than_zero_fire_counts.fire_count.max()))
  ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
  ax.set_title(plot_title)
  fig.supxlabel('(Gray: data not available)')
  fig.tight_layout()
  return fig, ax

def plot_counties_by_total_area_burned(counties_geo_df, keys, plot_title):
  fips_codes = get_state_fips_codes(keys)
  counties_geo_df = counties_geo_df[counties_geo_df['STATEFP'].isin(fips_codes)]
  zero_acres_burned = counties_geo_df[counties_geo_df.acres_burned == 0]
  more_than_zero_acres_burned = counties_geo_df[counties_geo_df.acres_burned > 0]
  fig, ax = plt.subplots(figsize=[12, 8])
  zero_acres_burned.plot(ax=ax, color='grey', legend=True, aspect=1)
  more_than_zero_acres_burned.plot(ax=ax, column='acres_burned', legend=True, norm=LogNorm(vmin=more_than_zero_acres_burned.acres_burned.min(), vmax=more_than_zero_acres_burned.acres_burned.max()))
  ax.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
  ax.set_title(plot_title)
  fig.supxlabel('(Gray: data not available)')
  fig.tight_layout()
  return fig, ax

def plot_causes_of_fires_by_number_of_fires(fires_df, keys, plot_title):
  state_fips_codes = get_state_fips_codes(keys)
  cause_counts_df = fires_df[fires_df.state_fips_code.isin(state_fips_codes)].value_counts('stat_cause_descr').reset_index()
  total_count = len(fires_df)
  # group small categories into "Other (aggregate)" for categories at less than 1.5 percent
  cause_counts_df.loc[cause_counts_df['count'] / total_count < 0.015, 'stat_cause_descr'] = 'Other (aggregate)'
  cause_counts = cause_counts_df.groupby('stat_cause_descr')['count'].sum().sort_values(ascending=False)
  cause_counts.name = None
  fig, ax = plt.subplots(figsize=[12, 8])
  cause_counts.plot.pie(ax=ax, title=plot_title, autopct=lambda pct: f'{pct / 100 * total_count:,.0f}', colormap=plt.cm.tab20)
  fig.supxlabel(f'(Total: {total_count:,} fires)')
  fig.tight_layout()
  return fig, ax

def plot_causes_of_fires_by_total_area_burned(fires_df, keys, plot_title):
  state_fips_codes = get_state_fips_codes(keys)
  cause_areas_df = fires_df[fires_df.state_fips_code.isin(state_fips_codes)].groupby('stat_cause_descr')['fire_size'].sum().reset_index()
  total_sum = fires_df['fire_size'].sum()
  # group small categories into "Other (aggregate)" for categories at less than 1.5 percent
  cause_areas_df.loc[cause_areas_df['fire_size'] / total_sum < 0.015, 'stat_cause_descr'] = 'Other (aggregate)'
  cause_areas = cause_areas_df.groupby('stat_cause_descr')['fire_size'].sum().sort_values(ascending=False)
  cause_areas.name = None
  fig, ax = plt.subplots(figsize=[12, 8])
  cause_areas.plot.pie(ax=ax, title=plot_title, autopct=lambda pct: f'{pct / 100 * total_sum:,.0f}', colormap=plt.cm.tab20)
  fig.supxlabel(f'(Total: {total_sum:,.0f} acres)')
  fig.tight_layout()
  return fig, ax
