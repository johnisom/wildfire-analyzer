from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame, Title, Subtitle

class WelcomeFrame(NotebookFrame):
  title = 'Welcome'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    title = Title(self, text='Welcome')
    intro_text = 'Welcome to Wildfire Analyzer! This application is a data analytics application for wildfires in the US.\n' \
      'Other than this welcome page, there are 4 pages: Plots, Predictions, Credits, and License.'
    intro_text_label = ttk.Label(self, text=intro_text, wraplength=630, justify=LEFT)
    plots_subtitle = Subtitle(self, text='Plots')
    plots_text = 'In the plots page you can plot pie charts of the causes of wildfires (such as lightning or arson) by number of fires started or by number of acres burned.\n' \
      'You can also plot a map of the US showing individual counties to show the number of fires per county or the acres burned by fires in that county.\n' \
      'To filter the results, you can specify a year range, and also which region of the US to show data for. Additionally, there\'s the option to filter on a per-state basis.'
    plots_text_label = ttk.Label(self, text=plots_text, wraplength=630, justify=LEFT)
    predictions_subtitle = Subtitle(self, text='Predictions')
    predictions_text = 'Here you\'ll be able to predict the likely cause of a fire by giving the machine learning model some information about the fire: final size, county location, and date of discovery.\n' \
      'The performance is 60.93% accuracy for the Longitude/Latitude model and 57.64% for the State/County model with 13 labels to choose from. That is actually rather good (random chance would be 7.69%).'
    predictions_text_label = ttk.Label(self, text=predictions_text, wraplength=630, justify=LEFT)
    credits_subtitle = Subtitle(self, text='Credits / License')
    credits_text = 'The credits and license pages have more information about the author of the project, the license used, and credits for others where credits are due.'
    credits_text_label = ttk.Label(self, text=credits_text, wraplength=630, justify=LEFT)

    # Set items on the grid
    title.grid(row=0, column=0, sticky=(N, E, W))
    intro_text_label.grid(row=1, column=0, sticky=EW)
    plots_subtitle.grid(row=2, column=0, sticky=EW)
    plots_text_label.grid(row=3, column=0, sticky=EW)
    predictions_subtitle.grid(row=4, column=0, sticky=EW)
    predictions_text_label.grid(row=5, column=0, sticky=EW)
    credits_subtitle.grid(row=6, column=0, sticky=EW)
    credits_text_label.grid(row=7, column=0, sticky=(S, E, W))
