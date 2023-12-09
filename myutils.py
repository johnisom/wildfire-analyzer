def add_fire_count_to_counties(geoid_indexed_counties, fires_df):
  counts = fires_df.value_counts('combined_fips_code')
  geoid_indexed_counties['fire_count'] = 0
  for fips_code, count in counts.items():
    geoid_indexed_counties.loc[fips_code, 'fire_count'] = count

def add_acres_burned_to_counties(geoid_indexed_counties, fires_df):
  sums = fires_df.groupby('combined_fips_code')['fire_size'].sum()
  geoid_indexed_counties['acres_burned'] = 0.0
  for fips_code, acres_burned in sums.items():
    geoid_indexed_counties.loc[fips_code, 'acres_burned'] = acres_burned
