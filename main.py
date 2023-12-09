import sqlite3
import pandas as pd
from fire_plotting import plot_causes_of_fires_by_state, plot_counties_by_number_of_fires, plot_counties_by_total_area_burned
from myutils import get_min_max_fire_years, add_fire_count_to_counties, add_acres_burned_to_counties
from state_and_county_info import COUNTIES
# from fire_size_prediction import create_trained_model_and_datasets

DB_FILENAME = 'db/fires.sqlite'

# # db connection stuff
con = sqlite3.connect(f'file:{DB_FILENAME}?mode=ro', uri=True)
fires_df = pd.read_sql_query(f'SELECT * FROM fires', con)
con.close()
min_year, max_year = get_min_max_fire_years(fires_df)
ranged_fires_df = fires_df[fires_df['fire_year'].between(min_year, max_year)]

plot_causes_of_fires_by_state(ranged_fires_df, 'lower48', 'Title')
counties_geo_df = COUNTIES.set_index('GEOID')
add_fire_count_to_counties(counties_geo_df, ranged_fires_df)
add_acres_burned_to_counties(counties_geo_df, ranged_fires_df)
plot_title = f'Number of reported wildfires in the US by county between {min_year} and {max_year}'
plot_counties_by_number_of_fires(counties_geo_df, 'lower48', plot_title)
plot_title = f'Number of reported acres burned by wildfires in the US by county between {min_year} and {max_year}'
plot_counties_by_total_area_burned(counties_geo_df, 'lower48', plot_title)

# # non-descriptive method
# model, X_train, X_test, y_train, y_test = create_trained_model_and_datasets(dataset)
