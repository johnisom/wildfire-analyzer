from tkinter import *
from tkinter import ttk

class NotebookFrame(ttk.Frame):
  title = 'Page'
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.configure(borderwidth=2, relief=SUNKEN)
