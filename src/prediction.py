from threading import Lock
from pathlib import Path
import joblib

FIPS_MODEL_PATH = Path().parent / 'joblib-objects' / 'firesize-fipscode-discoverycontaineddates-causecode-classifier.joblib'
FIPS_ENCODER_PATH = Path().parent / 'joblib-objects' / 'fipscode-labelencoder.joblib'
LONLAT_MODEL_PATH = Path().parent / 'joblib-objects' / 'firesize-lonlat-discoverycontaineddates-causecode-classifier.joblib'

def joblib_objects_unpacked():
  return FIPS_MODEL_PATH.is_file() and FIPS_ENCODER_PATH.is_file() and LONLAT_MODEL_PATH.is_file()

_fips_encoder = None
_fips_encoder_mutex = Lock()
def get_fips_encoder():
  global _fips_encoder
  global _fips_encoder_mutex
  with _fips_encoder_mutex:
    if _fips_encoder is None:
      _fips_encoder = joblib.load(FIPS_ENCODER_PATH)
  return _fips_encoder

_fips_model = None
_fips_model_mutex = Lock()
def get_fips_model():
  global _fips_model
  global _fips_model_mutex
  with _fips_model_mutex:
    if _fips_model is None:
      _fips_model = joblib.load(FIPS_MODEL_PATH)
  return _fips_model

_lonlat_model = None
_lonlat_model_mutex = Lock()
def get_lonlat_model(): 
  global _lonlat_model
  global _lonlat_model_mutex
  with _lonlat_model_mutex:
    if _lonlat_model is None:
      _lonlat_model = joblib.load(LONLAT_MODEL_PATH)
  return _lonlat_model
