import sqlite3
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from ./fire_size_prediction import create_trained_model_and_datasets
import matplotlib.pyplot as plt
import pygris
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

DB_FILENAME = 'db/fires.sqlite'

# db connection stuff
con = sqlite3.connect(f'file:{DB_FILENAME}?mode=ro', uri=True)
dataframe = pd.read_sql_query(f'SELECT * FROM fires', con)
con.close()

# non-descriptive method
model, X_train, X_test, y_train, y_test = create_trained_model_and_datasets(dataset)

# plot counties

counties = pygris.counties()
polys = []
for poly in counties.geometry:
  if type(poly) == Polygon:
    polys.append(poly)
  elif type(poly) == MultiPolygon:
    for p in poly.geoms:
      polys.append(p)

for poly in polys:
  plt.plot(*poly.exterior.xy)

plt.axis('square')
plt.show()