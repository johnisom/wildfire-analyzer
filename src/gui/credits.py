from pathlib import Path
from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame, Title, Subtitle

class CreditsFrame(NotebookFrame):
  title = 'Credits'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    title = Title(self, text='Credits')

    # Set items on the grid
    title.grid(row=0, column=0, sticky=(N, E, W))

class LicenseFrame(NotebookFrame):
  title = 'License'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    title = Title(self, text='The MIT License (MIT)')
    license_text = ''
    with open(Path().parent.parent / 'LICENSE', mode='r', encoding='utf-8') as f:
      license_text = f.read().strip()
    license = Text(self, width=78)
    license.insert(END, license_text)
    license.configure(state=DISABLED)

    # Set items on the grid
    title.grid(row=0, column=0, sticky=(N, E, W), pady='3')
    license.grid(row=1, column=0, sticky=(S, E, W))

