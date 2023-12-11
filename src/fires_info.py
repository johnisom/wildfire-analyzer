import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path().parent / 'db' / 'fires.sqlite'

_fires_df = None

def get_fires_dataframe():
  global _fires_df
  if _fires_df is None:
    print('Loading data on 1.88 million fires...')
    con = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True)
    _fires_df = pd.read_sql_query('SELECT * FROM fires', con)
    con.close()
  return _fires_df
