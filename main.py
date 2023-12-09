import sqlite3
import pandas as pd
from fire_plotting import plot_causes_of_fires_by_state, plot_counties_by_number_of_fires, plot_counties_by_total_area_burned
from myutils import add_fire_count_to_counties, add_acres_burned_to_counties
from state_and_county_info import get_all_counties
# from fire_size_prediction import create_trained_model_and_datasets

DB_FILENAME = 'db/fires.sqlite'

_fires_df = None

def get_fires_dataframe():
  global _fires_df
  if _fires_df is None:
    con = sqlite3.connect(f'file:{DB_FILENAME}?mode=ro', uri=True)
    _fires_df = pd.read_sql_query(f'SELECT * FROM fires', con)
    con.close()
  return _fires_df.copy()

def plot_fire_causes(year_start=None, year_end=None):
  fires_df = get_fires_dataframe()
  if year_start is None:
    year_start = fires_df.fire_year.min()
  if year_end is None: 
    year_end = fires_df.fire_year.max()
  fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
  plot_title = f'Number of reported wildfires in the US by fire cause between {year_start} and {year_end}'
  plot_causes_of_fires_by_state(fires_df, 'lower48', plot_title)

def plot_fire_counts(year_start=None, year_end=None):
  fires_df = get_fires_dataframe()
  if year_start is None:
    year_start = fires_df.fire_year.min()
  if year_end is None: 
    year_end = fires_df.fire_year.max()
  fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
  counties_geo_df = get_all_counties().set_index('GEOID')
  add_fire_count_to_counties(counties_geo_df, fires_df)
  plot_title = f'Number of reported wildfires in the US by county between {year_start} and {year_end}'
  plot_counties_by_number_of_fires(counties_geo_df, 'lower48', plot_title)

def plot_fire_area_burned(year_start=None, year_end=None):
  fires_df = get_fires_dataframe()
  if year_start is None:
    year_start = fires_df.fire_year.min()
  if year_end is None: 
    year_end = fires_df.fire_year.max()
  fires_df = fires_df[fires_df['fire_year'].between(year_start, year_end)]
  counties_geo_df = get_all_counties().set_index('GEOID')
  add_acres_burned_to_counties(counties_geo_df, fires_df)
  plot_title = f'Number of reported acres burned by wildfires in the US by county between {year_start} and {year_end}'
  plot_counties_by_total_area_burned(counties_geo_df, 'lower48', plot_title)


# # non-descriptive method
# model, X_train, X_test, y_train, y_test = create_trained_model_and_datasets(dataset)
