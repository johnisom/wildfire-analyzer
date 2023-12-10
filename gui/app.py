from tkinter import *
from tkinter import ttk
from .plots import PlotsFrame
from .predictions import PredictionsFrame
from .credits import CreditsFrame

class App(Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.title('WGU Capstone')

    # Set up the notebook and the frames in the notebook
    self.notebook = ttk.Notebook(self)
    self.plots_frame = PlotsFrame(self.notebook)
    self.predictions_frame = PredictionsFrame(self.notebook)
    self.credits_frame = CreditsFrame(self.notebook)
    self.notebook.add(self.plots_frame, text=self.plots_frame.title)
    self.notebook.add(self.predictions_frame, text=self.predictions_frame.title)
    self.notebook.add(self.credits_frame, text=self.credits_frame.title)

    # Set up the grid
    self.notebook.grid(row=0, column=0, sticky=NSEW)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
