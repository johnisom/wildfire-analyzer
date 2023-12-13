import sqlite3
import pandas as pd
from pathlib import Path
from threading import Lock

DB_PATH = Path().parent / 'db' / 'fires.sqlite'

_fires_mutex = Lock()
_fires_df = None
def get_fires_dataframe():
  global _fires_df
  global _fires_mutex
  with _fires_mutex:
    if _fires_df is None:
      con = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
      _fires_df = pd.read_sql_query('SELECT * FROM fires', con)
      con.close()
  return _fires_df
