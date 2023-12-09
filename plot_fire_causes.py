import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
from myutils import get_min_max_fire_years
from state_and_county_info import get_state_fips_codes

def plot_causes_of_fires_by_state(dataframe, keys, plot_title):
  state_fips_codes = get_state_fips_codes(keys)
  relevant_df = dataframe[dataframe.state_fips_code.isin(state_fips_codes)]
  df = relevant_df.value_counts('stat_cause_descr')
  fig, ax = plt.subplots(figsize=[12, 8])
  df.plot.pie(ax=ax, title=plot_title, legend=True)
  fig.tight_layout()
  plt.show()

con = sqlite3.connect('db/fires.sqlite')
min_year, max_year = get_min_max_fire_years(con)
dataframe = pd.read_sql_query(f'SELECT state_fips_code, stat_cause_code, stat_cause_descr FROM fires WHERE fire_year BETWEEN {min_year} AND {max_year}', con)
con.close()
