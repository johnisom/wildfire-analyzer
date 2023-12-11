from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame, Title, DefaultEntry, DatetimeEntry

class PredictionsFrame(NotebookFrame):
  title = 'Predictions'

  @staticmethod
  def check_fire_size(newval):
    if newval == '': return True
    try:
      flt = float(newval)
      return flt >= 0
    except ValueError:
      return False

  @staticmethod
  def check_longitude(newval):
    try:
      if newval == '' or newval == '-': return True
      if len(newval) == 2 and newval[0] == '-' and (int(newval[1]) == 1 or int(newval[1]) >= 6): return True
      if len(newval) == 3 and newval[0] == '-' and int(newval[1]) == 1 and int(newval[2]) <= 8: return True
      flt = float(newval)
      return flt <= -65 and flt > -188
    except ValueError:
      return False

  @staticmethod
  def check_latitude(newval):
    try:
      if newval == '': return True
      if len(newval) == 1 and int(newval) >= 1 and int(newval) <= 7: return True
      flt = float(newval)
      return flt < 72 and flt >= 17
    except ValueError:
      return False

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    title = Title(self, text='Predictions')
    subframe = ttk.LabelFrame(self, text='Predict cause of fire in giving some parameters')

    input_frame = ttk.Frame(subframe, padding=5)
    discovery_datetime_label = ttk.Label(input_frame, text='Discovery datetime: ')
    self.discovery_datetime_entry = DatetimeEntry(input_frame)
    contained_datetime_label = ttk.Label(input_frame, text='Contained datetime: ')
    self.contained_datetime_entry = DatetimeEntry(input_frame)
    fire_size_label = ttk.Label(input_frame, text='Fire size (acres): ')
    self.fire_size_entry = DefaultEntry(input_frame, default_text='0.1', validate='key', validatecommand=(self.register(PredictionsFrame.check_fire_size), '%P'))
    state_label = ttk.Label(input_frame, text='State: ')
    state_var = StringVar()
    self.state_entry = ttk.Combobox(input_frame, textvariable=state_var)
    county_label = ttk.Label(input_frame, text='County: ')
    county_var = StringVar()
    self.county_entry = ttk.Combobox(input_frame, textvariable=county_var, state=DISABLED)
    latitude_label = ttk.Label(input_frame, text='Latitude: ')
    self.latitude_entry = DefaultEntry(input_frame, default_text='(optional)', validate='key', validatecommand=(self.register(PredictionsFrame.check_latitude), '%P'))
    longitude_label = ttk.Label(input_frame, text='Longitude: ')
    self.longitude_entry = DefaultEntry(input_frame, default_text='(optional)', validate='key', validatecommand=(self.register(PredictionsFrame.check_longitude), '%P'))

    # Set items on the grid
    title.grid(row=0, column=0, sticky=(N, E, W))
    subframe.grid(row=1, column=0, sticky=(N, S, E, W))
    input_frame.grid(row=0, column=0, sticky=(N, E, W))
    discovery_datetime_label.grid(row=0, column=0, sticky=E)
    self.discovery_datetime_entry.grid(row=0, column=1, sticky=W)
    contained_datetime_label.grid(row=1, column=0, sticky=E)
    self.contained_datetime_entry.grid(row=1, column=1, sticky=W)
    fire_size_label.grid(row=3, column=0, sticky=E)
    self.fire_size_entry.grid(row=3, column=1, sticky=W)
    state_label.grid(row=0, column=2, sticky=E)
    self.state_entry.grid(row=0, column=3, sticky=W)
    county_label.grid(row=1, column=2, sticky=E)
    self.county_entry.grid(row=1, column=3, sticky=W)
    latitude_label.grid(row=2, column=2, sticky=E)
    self.latitude_entry.grid(row=2, column=3, sticky=W)
    longitude_label.grid(row=3, column=2, sticky=E)
    self.longitude_entry.grid(row=3, column=3, sticky=W)

    # Configure the grid
    self.rowconfigure((0,), weight=1)
    self.rowconfigure((1,), weight=10)
    self.columnconfigure((0,), weight=1)
    subframe.rowconfigure((0,), weight=1)
    subframe.columnconfigure((0,), weight=1)
    input_frame.rowconfigure((0, 1, 2, 3), weight=1)
    input_frame.columnconfigure((0, 1, 2, 3), weight=1)
