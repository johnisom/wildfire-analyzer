from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame, Title, Subtitle

class CreditsFrame(NotebookFrame):
  title = 'Credits'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    title = Title(self, text='Credits')

    # Set items on the grid
    title.grid(row=0, column=0, sticky=NSEW)
