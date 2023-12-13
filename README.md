# Wildfire Analyzer

## Installation

Install git, install git lfs, then clone github repo to the computer.

Install miniconda, then run `conda env create --file environment.yml` in this directory. Then activate the environment with `conda activate wildfire-analyzer`.

## Running application

Make sure you have 5 GB of free memory first.

`python main.py`

## About

This project is a data analytics and prediction project that uses machine learning. It runs locally as a TK desktop application.

## Structure

stand alone app running on windows 10 with jupyter notebook and sqlite for data access.

## Credits

### Wildfires Dataset

The dataset I'm using is https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires/data. I cleaned and formatted the data and selected only that which I needed, greatly reducing size.

### County-level Mapping

Reverse geocoding is made possible through the `pygris` python package.
It is a package that downloads and reads the US Census Bureau's TIGRIS file on the shapes and locations of all counties and county equivalents in the USA, and I used that to place the location of latitude and longitude coordinates in specific counties, as part of my cleaning and formatting the data. It is also used to display the map under the "Plots" tab of this application.
