# from math import inf
# import sqlite3
# import pandas as pd
# import matplotlib.pyplot as plt
# from plotting import plot_causes_of_fires_by_number_of_fires, plot_causes_of_fires_by_total_area_burned, plot_counties_by_number_of_fires, plot_counties_by_total_area_burned
# from myutils import add_fire_count_to_counties, add_acres_burned_to_counties, negativize_positive_longitudes
# from state_and_county_info import get_all_counties
from gui.app import App

# DB_FILENAME = 'db/fires.sqlite'

# _fires_df = None

# def get_fires_dataframe():
#   global _fires_df
#   if _fires_df is None:
#     print('Loading data on 1.88 million fires...')
#     con = sqlite3.connect(f'file:{DB_FILENAME}?mode=ro', uri=True)
#     _fires_df = pd.read_sql_query(f'SELECT * FROM fires', con)
#     con.close()
#   return _fires_df.copy()

# def plot_fire_cause_counts(keys=('lower48',), year_start=None, year_end=None):
#   fires_df = get_fires_dataframe()
#   year_start = max(fires_df.fire_year.min(), year_start or -inf)
#   year_end = min(fires_df.fire_year.max(), year_end or inf)
#   if year_start > year_end:
#     raise ValueError(f'year_start is greater than year_end ({year_start} > {year_end})')
#   fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
#   plot_title = f'Number of reported wildfires in the US by fire cause between {year_start} and {year_end}'

#   plot_causes_of_fires_by_number_of_fires(fires_df, keys, plot_title)
#   plt.show()

# def plot_fire_cause_area_burned(keys=('lower48',), year_start=None, year_end=None):
#   fires_df = get_fires_dataframe()
#   year_start = max(fires_df.fire_year.min(), year_start or -inf)
#   year_end = min(fires_df.fire_year.max(), year_end or inf)
#   if year_start > year_end:
#     raise ValueError(f'year_start is greater than year_end ({year_start} > {year_end})')
#   fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
#   plot_title = f'Number of reported acres burned by wildfires in the US by fire cause between {year_start} and {year_end}'

#   plot_causes_of_fires_by_total_area_burned(fires_df, keys, plot_title)
#   plt.show()

# def plot_fire_county_counts(keys=('lower48',), year_start=None, year_end=None):
#   fires_df = get_fires_dataframe()
#   year_start = max(fires_df.fire_year.min(), year_start or -inf)
#   year_end = min(fires_df.fire_year.max(), year_end or inf)
#   if year_start > year_end:
#     raise ValueError(f'year_start is greater than year_end ({year_start} > {year_end})')
#   fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
#   counties_geo_df = get_all_counties().set_index('GEOID')

#   add_fire_count_to_counties(counties_geo_df, fires_df)
#   plot_title = f'Number of reported wildfires in the US by county between {year_start} and {year_end}'
#   plot_counties_by_number_of_fires(counties_geo_df, keys, plot_title)
#   plt.show()

# def plot_fire_county_area_burned(keys=('lower48',), year_start=None, year_end=None):
#   fires_df = get_fires_dataframe()
#   year_start = max(fires_df.fire_year.min(), year_start or -inf)
#   year_end = min(fires_df.fire_year.max(), year_end or inf)
#   if year_start > year_end:
#     raise ValueError(f'year_start is greater than year_end ({year_start} > {year_end})')
#   fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
#   counties_geo_df = get_all_counties().set_index('GEOID')

#   add_acres_burned_to_counties(counties_geo_df, fires_df)
#   plot_title = f'Number of reported acres burned by wildfires in the US by county between {year_start} and {year_end}'
#   plot_counties_by_total_area_burned(counties_geo_df, keys, plot_title)
#   plt.show()

# def plot_everything(keys=('lower48',), year_start=None, year_end=None):
#   fires_df = get_fires_dataframe()
#   year_start = max(fires_df.fire_year.min(), year_start or -inf)
#   year_end = min(fires_df.fire_year.max(), year_end or inf)
#   fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
#   counties_geo_df = get_all_counties().set_index('GEOID')
#   add_fire_count_to_counties(counties_geo_df, fires_df)
#   add_acres_burned_to_counties(counties_geo_df, fires_df)
#   fire_cause_counts_title = f'Number of reported wildfires in the US by fire cause between {year_start} and {year_end}'
#   fire_cause_area_burned_title = f'Number of reported acres burned by wildfires in the US by fire cause between {year_start} and {year_end}'
#   fire_counts_title = f'Number of reported wildfires in the US by county between {year_start} and {year_end}'
#   fire_area_burned_title = f'Number of reported acres burned by wildfires in the US by county between {year_start} and {year_end}'
#   plot_causes_of_fires_by_total_area_burned(fires_df, keys, fire_cause_area_burned_title)
#   plot_counties_by_total_area_burned(counties_geo_df, keys, fire_area_burned_title)
#   plot_causes_of_fires_by_number_of_fires(fires_df, keys, fire_cause_counts_title)
#   plot_counties_by_number_of_fires(counties_geo_df, keys, fire_counts_title)
#   plt.show()

App().mainloop()
