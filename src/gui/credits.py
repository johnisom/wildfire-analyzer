from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame

class CreditsFrame(NotebookFrame):
  title = 'Credits'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
