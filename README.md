# WGU Capstone Project

## Installation

Install miniconda, then run `conda env create --file environment.yml` in this directory. Then activate the environment with `conda activate wildfire-analyzer`.

## Running application

1. Unzip the `joblib-objects.zip` file into the project's top level. `unzip joblib-objects.zip`
2. `python main.py`

## About

This project is a data analytics and prediction project that uses machine learning. It runs in jupyter notebooks.

The dataset I'm using is https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires/data. I cleaned and formatted the data and selected only
that which I needed.
Reverse geocoding is made possible through the `pygris` python package. It is a package that downloads and reads the US Census Bureau's TIGRIS file on the shapes and locations of all counties and county equivalents in the USA, and I used that to place the location of latitude and longitude coordinates in specific counties, as part of my cleaning and formatting the data.

This is heavily work in progress and the requirements may change.

## Structure

stand alone app running on windows 10 with jupyter notebook and sqlite for data access.

## Requirements

make the following descriptive (analytical) methods:
1. table showing ranking of counties that have the most fires and most acres burned by fires, per year.
  a. alternatively, have it be a map with counties that are shaded according to number of fires (this is what i went with)
2. a pie chart that shows causes of wildfires in the US. the user can select an individual state if they wish, or all of the USA.
3. a confusion matrix to visualize the model's performance

make the following non-descriptive (predictive) methods:
1. model that predicts fire size class based off of some parameters
  a. suggested params are location (probably granular to county), date, reporting agency

## TODOS

There are 1,880,465 data points which need to be split into training and test sets.
