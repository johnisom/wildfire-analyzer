from threading import Lock
from pathlib import Path
from joblib import load as joblib_load
import pandas as pd

FIPS_MODEL_PATH = Path().parent / 'joblib-objects' / 'firesize-fipscode-discoverycontaineddates-causecode-classifier.joblib'
FIPS_ENCODER_PATH = Path().parent / 'joblib-objects' / 'fipscode-ordinalencoder.joblib'
LONLAT_MODEL_PATH = Path().parent / 'joblib-objects' / 'firesize-lonlat-discoverycontaineddates-causecode-classifier.joblib'
STAT_CAUSE_CODE_TO_DESCR = {
  1: 'Lightning', 2: 'Equipment Use', 3: 'Smoking', 4: 'Campfire', 5: 'Debris Burning',
  6: 'Railroad', 7: 'Arson', 8: 'Children', 9: 'Miscellaneous', 10: 'Fireworks',
  11: 'Powerline', 12: 'Structure', 13: 'Missing/Undefined'
}

def joblib_objects_present():
  return FIPS_MODEL_PATH.is_file() and FIPS_ENCODER_PATH.is_file() and LONLAT_MODEL_PATH.is_file()

_fips_encoder = None
_fips_encoder_mutex = Lock()
def get_fips_encoder():
  global _fips_encoder
  global _fips_encoder_mutex
  with _fips_encoder_mutex:
    if _fips_encoder is None:
      _fips_encoder = joblib_load(FIPS_ENCODER_PATH)
  return _fips_encoder

_fips_model = None
_fips_model_mutex = Lock()
def get_fips_model():
  global _fips_model
  global _fips_model_mutex
  with _fips_model_mutex:
    if _fips_model is None:
      _fips_model = joblib_load(FIPS_MODEL_PATH)
  return _fips_model

_lonlat_model = None
_lonlat_model_mutex = Lock()
def get_lonlat_model(): 
  global _lonlat_model
  global _lonlat_model_mutex
  with _lonlat_model_mutex:
    if _lonlat_model is None:
      _lonlat_model = joblib_load(LONLAT_MODEL_PATH)
  return _lonlat_model

def run_fips_model_prediction(fire_size, combined_fips_code, discovery_datetime, contained_datetime):
  encoder = get_fips_encoder()
  classifier = get_fips_model()
  encoded_fips_code = encoder.transform(pd.DataFrame(data=[[combined_fips_code]], columns=['combined_fips_code']))[0].astype(int)[0]
  df = pd.DataFrame(
    data=[[fire_size, encoded_fips_code, discovery_datetime.timestamp(), contained_datetime.timestamp()]],
    columns=['fire_size', 'combined_fips_code', 'discovery_datetime', 'contained_datetime']
  )
  probabilities = classifier.predict_proba(df)[0]
  return map_probabilities_to_causes(probabilities)

def run_lonlat_model_prediction(fire_size, longitude, latitude, discovery_datetime, contained_datetime):
  classifier = get_lonlat_model()
  df = pd.DataFrame(
    data=[[fire_size, longitude, latitude, discovery_datetime.timestamp(), contained_datetime.timestamp()]],
    columns=['fire_size', 'longitude', 'latitude', 'discovery_datetime', 'contained_datetime']
  )
  probabilities = classifier.predict_proba(df)[0]
  return map_probabilities_to_causes(probabilities)

def map_probabilities_to_causes(probabilities):
  probabilities_by_stat_cause_code = list(enumerate(probabilities, 1)) # add 1 back to the result, to make the mapping from 0-12 to 1-13
  probabilities_by_stat_cause_code.sort(key=lambda tup: tup[1], reverse=True)
  probabilities_by_stat_cause_descr = [(STAT_CAUSE_CODE_TO_DESCR[code], percent) for code, percent in probabilities_by_stat_cause_code]
  return probabilities_by_stat_cause_descr
