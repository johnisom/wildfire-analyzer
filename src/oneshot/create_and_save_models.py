import sqlite3
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump as joblib_dump
from pathlib import Path
from ..prediction import FIPS_MODEL_PATH, FIPS_ENCODER_PATH, LONLAT_MODEL_PATH

DB_PATH = Path().parent.parent / 'db' / 'fires.sqlite'

# TASK:
# Given a fire’s location, start and end date, and size, predict the cause of the fire.

def create_trained_lonlat_model_and_datasets(fires_df):
  """
  Given a dataframe of all data from the fires database, format and split the data for training and train a machine learning model.
  The machine learning model takes features fire_size, longitude, latitude, discovery_datetime and contained_datetime,
  and predicts stat_cause_code - 1.
  Returns the model and the split training and testing data.
  """
  df = fires_df[['fire_size', 'longitude', 'latitude', 'discovery_datetime', 'contained_datetime', 'stat_cause_code']]

  # Encode data for the model
  df.loc[:, ['stat_cause_code']] = df['stat_cause_code'] - 1 # change range from 1-13 to 0-12

  # Only train with good data
  df = df.dropna()

  X = df.drop(['stat_cause_code'], axis=1)
  y = df['stat_cause_code'].astype(int)

  # Split into test and training sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

  # These kwargs give best tradeoff between model performance and size.
  # Compared to default params, it reduces the size of the model by 13x yet only reduces performance by 1.6% (62.5% -> 60.93%)
  clf = RandomForestClassifier(n_estimators=18, max_samples=0.33, n_jobs=-1)
  clf.fit(X_train, y_train)
  return clf, X_train, X_test, y_train, y_test

def create_trained_fipscode_model_and_encoder_and_datasets(fires_df):
  """
  Given a dataframe of all data from the fires database, format and split the data for training and train a machine learning model.
  Returns the model, the combined fips code ordinal encoder, and the split training and testing data.
  """
  df = fires_df[['fire_size', 'combined_fips_code', 'discovery_datetime', 'contained_datetime', 'stat_cause_code']]

  # Encode data for the model
  combined_fips_code_oe = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
  df.loc[:, ['combined_fips_code']] = combined_fips_code_oe.fit_transform(df[['combined_fips_code']]).astype(int)
  df.loc[:, ['stat_cause_code']] = df['stat_cause_code'] - 1 # change range from 1-13 to 0-12

  # Only train with good data
  df = df.dropna()

  X = df.drop(['stat_cause_code'], axis=1)
  y = df['stat_cause_code'].astype(int)

  # Split into test and training sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

  # These kwargs reduce size of the model by >15x while actually improving test data performance by ~1%,
  # however, it reduces training data performance.
  clf = RandomForestClassifier(n_estimators=24, max_depth=20, max_samples=0.4, n_jobs=-1)
  clf.fit(X_train, y_train)
  return clf, combined_fips_code_oe, X_train, X_test, y_train, y_test

def train_and_save_fipscode_model_and_encoder(fires_df=None):
  if fires_df is None:
    con = sqlite3.connect(f'file:{DB_PATH}?ro', uri=True)
    print('Loading all fires from database...')
    fires_df = pd.read_sql_query('SELECT * FROM fires', con)
    con.close()
  clf, combined_fips_code_oe, *_ = create_trained_fipscode_model_and_encoder_and_datasets(fires_df)
  joblib_dump(clf, FIPS_MODEL_PATH, compress=9)
  joblib_dump(combined_fips_code_oe, FIPS_ENCODER_PATH, compress=9)

def train_and_save_lonlat_model(fires_df=None):
  if fires_df is None:
    con = sqlite3.connect(f'file:{DB_PATH}?ro', uri=True)
    print('Loading all fires from database...')
    fires_df = pd.read_sql_query('SELECT * FROM fires', con)
    con.close()
  clf, *_ = create_trained_lonlat_model_and_datasets(fires_df)
  joblib_dump(clf, LONLAT_MODEL_PATH, compress=9)

def train_and_save_both_models():
  con = sqlite3.connect(f'file:{DB_PATH}?ro', uri=True)
  print('Loading all fires from database...')
  fires_df = pd.read_sql_query('SELECT * FROM fires', con)
  con.close()
  print('Training and saving the FIPS code model and ordinal encoder...')
  train_and_save_fipscode_model_and_encoder(fires_df)
  print('Training and saving the longitude/latitude model...')
  train_and_save_lonlat_model(fires_df)
