import sqlite3
import pandas as pd
from fire_size_prediction import create_trained_model_and_datasets

# DB_FILENAME = 'db/fires.sqlite'

# # db connection stuff
# con = sqlite3.connect(f'file:{DB_FILENAME}?mode=ro', uri=True)
# dataframe = pd.read_sql_query(f'SELECT * FROM fires', con)
# con.close()

# # non-descriptive method
# model, X_train, X_test, y_train, y_test = create_trained_model_and_datasets(dataset)
