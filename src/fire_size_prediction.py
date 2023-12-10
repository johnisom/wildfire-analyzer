import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns
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

def create_trained_model_and_datasets(dataframe: pd.DataFrame) -> (LinearRegression, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series):
    """
    Given a dataframe of all data from the fires database, format and split the data for training and train a machine learning model.
    returns the model and the split training and testing data.
    """
    df = dataframe[:]
    df.loc[:, ['duration','week_day','day_of_month','month']] = None
    df.loc[df.contained_datetime.notna(), 'duration'] = df.contained_datetime - df.discovery_datetime
    df.loc[:, ['week_day']] = df.discovery_datetime.map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).weekday())
    df.loc[:, ['day_of_month']] = df.discovery_datetime.map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).day)
    df.loc[:, ['month']] = df.discovery_datetime.map(lambda timestamp: datetime.datetime.fromtimestamp(timestamp).month)
    df.set_index('discovery_datetime')

    state_fips_code_encoder = LabelEncoder()
    county_fips_code_encoder = LabelEncoder()
    combined_fips_code_encoder = LabelEncoder()

    df.loc[:, ['state_fips_code']] = state_fips_code_encoder.fit_transform(df.loc[:, ['state_fips_code']])
    df.loc[:, ['county_fips_code']] = county_fips_code_encoder.fit_transform(df.loc[:, ['county_fips_code']])
    df.loc[:, ['combined_fips_code']] = combined_fips_code_encoder.fit_transform(df.loc[:, ['combined_fips_code']])

    df = df.dropna()

    X = df[INDEPENDENT_VARIABLES] # TODO: figure this out. Unable to perform a single logistic regression because nothing converges, no matter the solver.
    y = df[DEPENDENT_VARIABLE]

    # Split discovery_datetime into day of week, week of year and use those.

    # Encode non-numeric features
    # reporting_agency_encoder = LabelEncoder()
    # X.loc[:, 'nwcg_reporting_agency'] = reporting_agency_encoder.fit_transform(X.nwcg_reporting_agency)

    # Split into test and training sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Run the logistic regression
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test
