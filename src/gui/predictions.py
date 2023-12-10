from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame

class PredictionsFrame(NotebookFrame):
  title = 'Predictions'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
