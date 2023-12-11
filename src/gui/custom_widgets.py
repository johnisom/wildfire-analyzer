from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import datetime

class NotebookFrame(ttk.Frame):
  title = 'Page'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs, borderwidth=2, relief=SUNKEN, padding=5)

class DefaultEntry(ttk.Entry):
  def __init__(self, master=None, default_text='', **kwargs):
    super().__init__(master=master, **kwargs)

    self.default_text = default_text
    self.showing_default_text = True
    self.on_exit()
    self.bind('<FocusIn>', self.on_entry)
    self.bind('<FocusOut>', self.on_exit)

  def on_entry(self, *_):
    if self.showing_default_text:
      self.delete(0, END)
      self.config(foreground='black')
      self.showing_default_text = False
  
  def on_exit(self, *_):
    if self.get() == '':
      self.showing_default_text = True
      self.insert(0, self.default_text)
      self.config(foreground='grey')

  def get_value(self):
    return '' if self.showing_default_text else self.get()

class DatetimeEntry(ttk.Frame):
  @staticmethod
  def check_hour(newval):
    if newval == '' or newval == 'HH': return True
    return newval.isdigit() and int(newval) >= 1 and int(newval) <= 12

  @staticmethod
  def check_min(newval):
    if newval == '' or newval == 'MM': return True
    return newval.isdigit() and int(newval) >= 0 and int(newval) <= 59

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.date_entry = DateEntry(self)
    hour_entry_label=ttk.Label(self, text='@')
    self.hour_entry = DefaultEntry(self, default_text='HH', width=3, justify=RIGHT, validate='key', validatecommand=(self.register(DatetimeEntry.check_hour), '%P'))
    minute_entry_label=ttk.Label(self, text=':')
    self.minute_entry = DefaultEntry(self, default_text='MM', width=4, justify=RIGHT, validate='key', validatecommand=(self.register(DatetimeEntry.check_min), '%P'))
    ampm_entry_label=ttk.Label(self, text=' ')
    self.ampm_entry = ttk.Combobox(self, values=('AM', 'PM'), width=3, validate='key', validatecommand=(self.register(lambda *a: False), '%P'))
    self.ampm_entry.current(0)

    # Set items on the grid
    self.date_entry.grid(row=0, column=0, sticky=E)
    hour_entry_label.grid(row=0, column=1)
    self.hour_entry.grid(row=0, column=2, sticky=EW)
    minute_entry_label.grid(row=0, column=3)
    self.minute_entry.grid(row=0, column=4, sticky=EW)
    ampm_entry_label.grid(row=0, column=5)
    self.ampm_entry.grid(row=0, column=6, sticky=W)

  def get_datetime(self):
    date = self.date_entry.get_date()
    time = self.get_time()
    return datetime.datetime.combine(date, time)

  def get_time(self):
    hour = int(self.hour_entry.get_value() or 0)
    minute = int(self.minute_entry.get_value() or 0)
    ampm = self.ampm_entry.get().upper()
    if ampm == 'AM' and hour == 12:
      hour = 0
    elif ampm == 'PM' and hour >= 1 and hour <= 11:
      hour += 12
    return datetime.time(hour, minute)

class Title(ttk.Label):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs, font=('Helvetica', 20))

class Subtitle(ttk.Label):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs, font=('Helvetica', 15))
