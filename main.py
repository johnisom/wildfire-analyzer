import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

DB_FILENAME = 'db/fires.sqlite'

# TODO: redo this section
COL_NAMES = [
  'objectid', # 0
  'nwcg_reporting_agency', # 1
  'nwcg_reporting_unit_id', # 2
  'nwcg_reporting_unit_name', # 3
  'fire_year', # 4
  'discovery_datetime', # 5
  'stat_cause_code', # 6
  'stat_cause_descr', # 7
  'cont_datetime', # 8
  'latitude', # 9
  'longitude', # 10
  'owner_code', # 11
  'owner_descr', # 12
  'state', # 13
  'county', # 14
  'fips_code', # 15
  'fips_name', # 16
  'fire_size', # 17
  'fire_size_class' # 18
]
INDEPENDENT_VARIABLES = [COL_NAMES[i] for i in (2,5,6,9,10,13,15)]
DEPENDENT_VARIABLE = COL_NAMES[18]

# db connection stuff
con = sqlite3.connect(f'file:{DB_FILENAME}?mode=ro', uri=True)
dataset = pd.read_sql_query(f'SELECT * FROM fires', con)
con.commit()
con.close()

X = dataset[INDEPENDENT_VARIABLES].values
y = dataset[DEPENDENT_VARIABLE].values

# Clean up NaN values
# imputer = impute.SimpleImputer(missing_value=np.nan, strategy='mean')
# imputer.fit(X[:, 1:6])
# X[:, 1:6] = imputer.transform(X[:, 1:6])

# Encode non-numeric features
non_numeric_feature_indices = [] # TODO
ct = ColumnTransformer(transformers=[('reporting_unit_encoder', LabelEncoder(), [0]), ('state_encoder', LabelEncoder(), [5])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

# Run the logistic regression
model = linear_model.LogisticRegression()
model.fit(X, y)

