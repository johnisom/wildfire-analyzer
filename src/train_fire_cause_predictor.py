import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import datetime

# INDEPENDENT_VARIABLES = ['nwcg_reporting_agency', 'discovery_datetime', 'combined_fips_code']
# DEPENDENT_VARIABLE = 'fire_size'

INDEPENDENT_VARIABLES = [
    'fire_year',
    'discovery_datetime',
    'contained_datetime',
    'fire_size',
    'longitude',
    'latitude',
    'state_fips_code',
    'county_fips_code',
    'combined_fips_code',
    'duration',
    'week_day',
    'day_of_month',
    'month'
]
DEPENDENT_VARIABLE = 'stat_cause_code'

# TASK:
# Given a fire’s location, date, and the agency that reported the fire, predict the final
# contained fire size class of the fire.

def create_trained_model_and_datasets(dataframe):
  """
  Given a dataframe of all data from the fires database, format and split the data for training and train a machine learning model.
  returns the model and the split training and testing data.
  """
  df = dataframe.copy()
  df.loc[:, ['duration','week_day','month']] = None
  df.loc[df.contained_datetime.notna(), 'duration'] = df.contained_datetime - df.discovery_datetime
  df.loc[:, ['week_day']] = df.discovery_datetime.map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).weekday())
  df.loc[:, ['day_of_month']] = df.discovery_datetime.map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).day)
  df.loc[:, ['month']] = df.discovery_datetime.map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).month)
  df = df[['fire_year', 'stat_cause_descr', 'fire_size', 'latitude', 'longitude', 'county_fips_name', 'state_alpha_code', 'duration', 'week_day', 'month']]

  state_alpha_code_encoder = LabelEncoder() # potentially use combined fips code?
  county_fips_name_encoder = LabelEncoder() # potentially use combined fips code?
  stat_cause_descr_label_encoder = LabelEncoder()

  df.loc[:, ['state_alpha_code']] = state_alpha_code_encoder.fit_transform(df['state_alpha_code'])
  df.loc[:, ['county_fips_name']] = county_fips_name_encoder.fit_transform(df['county_fips_name'])
  df.loc[:, ['stat_cause_descr']] = stat_cause_descr_label_encoder.fit_transform(df['stat_cause_descr']).astype(int)

  df = df.dropna() # NOTE: optional to do this, should analyze performance with and without it

  X = df.drop(['stat_cause_descr'], axis=1).values
  y = df['stat_cause_descr'].values

  # Split into test and training sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

  # clf_xgboost = xgb.XGBClassifier(objective='multi:softprob')
  # clf_xgboost.fit(X_train, y_train)
  clf = RandomForestClassifier(n_estimators=100)
  clf.fit(X_train, y_train)
  # predicted = clf_xgboost.predict(X_test)
  predicted = clf.predict(X_test)
  accuracy = np.mean(predicted == y_test)

  # Run the logistic regression
  # model = LinearRegression()
  # model.fit(X_train, y_train)

  # return clf_xgboost, X_train, X_test, y_train, y_test
  return clf, X_train, X_test, y_train, y_test
