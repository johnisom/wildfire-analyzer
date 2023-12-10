from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame

class WelcomeFrame(NotebookFrame):
  title = 'Welcome'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
