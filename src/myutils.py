from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from shapely.affinity import translate

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

def translate_poly_or_multipoly(geometry):
  if type(geometry) == Polygon:
    return translate(geometry, xoff=-360)
  elif type(geometry) == MultiPolygon:
    polys = []
    for poly in geometry.geoms:
      if poly.bounds[0] > 0:
        polys.append(translate_poly_or_multipoly(poly))
      else:
        polys.append(poly)
    return MultiPolygon(polys)

def negativize_positive_longitudes(counties):
  geoms_needing_changing = {}
  for _iter_idx, (idx, geometry) in counties.geometry.reset_index().iterrows():
    if geometry.bounds[0] > 0 or geometry.bounds[2] > 0:
      geoms_needing_changing[idx] = translate_poly_or_multipoly(geometry)
  for idx, geometry in geoms_needing_changing.items():
    counties.loc[idx, 'geometry'] = geometry