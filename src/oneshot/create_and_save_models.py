import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump as joblib_dump
from pathlib import Path
from ..prediction import FIPS_MODEL_PATH, FIPS_ENCODER_PATH, LONLAT_MODEL_PATH

DB_FILENAME = 'db/fires.sqlite'

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
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

  clf = RandomForestClassifier(n_estimators=100)
  clf.fit(X_train, y_train)
  return clf, X_train, X_test, y_train, y_test

def create_trained_fipscode_model_and_encoder_and_datasets(fires_df):
  """
  Given a dataframe of all data from the fires database, format and split the data for training and train a machine learning model.
  Returns the model, the combined fips code label encoder, and the split training and testing data.
  """
  df = fires_df[['fire_size', 'combined_fips_code', 'discovery_datetime', 'contained_datetime', 'stat_cause_code']]

  # Encode data for the model
  combined_fips_code_le = LabelEncoder()
  df.loc[:, ['combined_fips_code']] = combined_fips_code_le.fit_transform(df['combined_fips_code'])
  df.loc[:, ['stat_cause_code']] = df['stat_cause_code'] - 1 # change range from 1-13 to 0-12

  # Only train with good data
  df = df.dropna()

  X = df.drop(['stat_cause_code'], axis=1)
  y = df['stat_cause_code'].astype(int)

  # Split into test and training sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

  clf = RandomForestClassifier(n_estimators=100)
  clf.fit(X_train, y_train)
  return clf, combined_fips_code_le, X_train, X_test, y_train, y_test

def train_and_save_fipscode_model_and_encoder(fires_df):
  clf, combined_fips_code_le, *_ = create_trained_fipscode_model_and_encoder_and_datasets(fires_df)
  joblib_dump(clf, FIPS_MODEL_PATH)
  joblib_dump(combined_fips_code_le, FIPS_ENCODER_PATH)

def train_and_save_lonlat_model(fires_df):
  clf, *_ = create_trained_lonlat_model_and_datasets(fires_df)
  joblib_dump(clf, LONLAT_MODEL_PATH)

def train_and_save_both_models():
  con = sqlite3.connect(f'file:{DB_FILENAME}?ro', uri=True)
  print('Loading all fires from database...')
  fires_dataframe = pd.read_sql_query('SELECT * FROM fires', con)
  con.close()
  print('Training and saving the FIPS code model and label encoder...')
  train_and_save_fipscode_model_and_encoder(fires_dataframe)
  print('Training and saving the longitude/latitude model...')
  train_and_save_lonlat_model(fires_dataframe)
