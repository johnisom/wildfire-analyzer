from tkinter import *
from tkinter import ttk

class NotebookFrame(ttk.Frame):
  title = 'Page'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.configure(borderwidth=2, relief=SUNKEN, padding=5)

class DefaultEntry(ttk.Entry):
  def __init__(self, master=None, default_text='', **kwargs):
    super().__init__(master=master, **kwargs)

    self.default_text = default_text
    self.showing_default_text = True
    self.on_exit()
    self.bind('<FocusIn>', self.on_entry)
    self.bind('<FocusOut>', self.on_exit)

  def on_entry(self, e=None):
    if self.showing_default_text:
      self.delete(0, END)
      self.config(foreground='black')
      self.showing_default_text = False
  
  def on_exit(self, e=None):
    if self.get() == '':
      self.showing_default_text = True
      self.insert(0, self.default_text)
      self.config(foreground='grey')

  def get_value(self):
    return '' if self.showing_default_text else self.get()

class Title(ttk.Label):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # TODO
    self.configure(font=('Helvetica', 20))

class Subtitle(ttk.Label):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # TODO
    self.configure(font=('Helvetica', 15))
