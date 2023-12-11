from src.gui.app import App
from threading import Thread
from src.fires_info import get_fires_dataframe
from src.location_info import get_counties_geodf,get_fips_codes_dataframe
from src.prediction import get_fips_encoder, get_fips_model, get_lonlat_model, joblib_objects_unpacked

# Load the database data and pygris geographical data in the background
def fires_info_thread_target():
  print('Starting thread to load fires info...')
  get_fires_dataframe()
  print('...Finished loading fires info.')
def location_info_thread_target():
  print('Starting thread to load location info...')
  get_fips_codes_dataframe()
  get_counties_geodf()
  print('...Finished loading location info.')
fires_info_thread = Thread(target=fires_info_thread_target)
location_info_thread = Thread(target=location_info_thread_target)

fires_info_thread.start()
location_info_thread.start()

enable_ml = joblib_objects_unpacked()
if enable_ml:
  # Load the ML prediction models in the background
  def prediction_thread_target():
    print('Starting thread to load ML models...')
    get_fips_encoder()
    get_fips_model()
    get_lonlat_model()
    print('...Finished loading ML models.')
  prediction_thread = Thread(target=prediction_thread_target)
  prediction_thread.start()

tk_app = App(enable_predictions=enable_ml)
tk_app.mainloop()
