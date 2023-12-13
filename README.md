# Wildfire Analyzer

This is a data analytics and prediction application that uses machine learning. It runs locally as a TK desktop application. Its purpose is to aid in the analysis of wildfires in the US through reviewing historical data and by making predictions of causes of wildfires.

## Installation

Install these applications:
- `git`: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
  - If you already have git installed (`git` is a command in your terminal), skip this step.
- `git-lfs`: https://git-lfs.com/
  - If you already have git-lfs installed (`git lfs` is a command inyour terminal), skip this step.
- `miniconda`: https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html
  - If you already have miniconda or anaconda installed (`conda` is a command in your terminal), skip this step.

Next, in a terminal with miniconda active (`conda` is a useable command), clone the repository, pull the git-lfs files, and install python package dependencies:
```sh
git clone https://github.com/johnisom/wgucapstone.git wildfire-analyzer
cd wildfire-analyzer
git lfs pull
conda env create --file environment.yml
conda activate wildfire-analyzer
```

The application is now installed and ready to use.

## Running application

Prerequisite: 3.5 GB of free memory.

In a terminal with miniconda, activate the miniconda environment: `conda activate wildfire-analyzer`.
Then, navigate to this directory (`cd wildfire-analyzer`).
  
Finally, run the application by running this command: `python main.py`.

The GUI will start up immediately, and the datasets and predictive models will load in the background.

## Credits

### Wildfires Dataset

The dataset I'm using is https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires/data. I cleaned and formatted the data and selected only that which I needed, greatly reducing size.

### County-level Mapping

Reverse geocoding is made possible through the `pygris` python package.
It is a package that downloads and reads the US Census Bureau's TIGRIS file on the shapes and locations of all counties and county equivalents in the USA, and I used that to place the location of latitude and longitude coordinates in specific counties, as part of my cleaning and formatting the data. It is also used to display the map under the "Plots" tab of this application.
