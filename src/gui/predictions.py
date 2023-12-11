from tkinter import *
from tkinter import ttk
from .custom_widgets import NotebookFrame, Title, DefaultEntry, DatetimeEntry
from ..state_and_county_info import get_fips_codes_dataframe

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

    self.set_up_state_county_variables()

    title = Title(self, text='Predictions')
    subframe = ttk.LabelFrame(self, text='Predict cause of fire in giving some parameters')

    input_frame = ttk.Frame(subframe, padding=5)
    discovery_datetime_label = ttk.Label(input_frame, text='Discovery datetime: ')
    self.discovery_datetime_entry = DatetimeEntry(input_frame)
    contained_datetime_label = ttk.Label(input_frame, text='Contained datetime: ')
    self.contained_datetime_entry = DatetimeEntry(input_frame)
    fire_size_label = ttk.Label(input_frame, text='Fire size (acres): ')
    self.fire_size_entry = DefaultEntry(input_frame, default_text='0.1', validate='key', validatecommand=(self.register(PredictionsFrame.check_fire_size), '%P'))
    location_input_frame = ttk.LabelFrame(input_frame, text='Fill in either State/County or Longitude/Latitude', padding='0 2 0 5')
    state_label = ttk.Label(location_input_frame, text='State: ')
    self.state_var = StringVar()
    self.state_entry = ttk.Combobox(location_input_frame, textvariable=self.state_var, values=self.state_names(), validate='key', validatecommand=(self.register(lambda *_: False), '%P'))
    self.state_entry.current(0)
    self.state_entry.bind('<<ComboboxSelected>>', self.handle_state_selected)
    county_label = ttk.Label(location_input_frame, text='County: ')
    self.county_var = StringVar()
    self.county_entry = ttk.Combobox(location_input_frame, textvariable=self.county_var, state=DISABLED, validate='key', validatecommand=(self.register(lambda *_: False), '%P'))
    location_separator = ttk.Separator(location_input_frame, orient=VERTICAL)
    longitude_label = ttk.Label(location_input_frame, text='Longitude: ')
    self.longitude_entry = DefaultEntry(location_input_frame, default_text='-102.674', validate='key', validatecommand=(self.register(PredictionsFrame.check_longitude), '%P'))
    latitude_label = ttk.Label(location_input_frame, text='Latitude: ')
    self.latitude_entry = DefaultEntry(location_input_frame, default_text='42.124', validate='key', validatecommand=(self.register(PredictionsFrame.check_latitude), '%P'))

    # Set items on the grid
    title.grid(row=0, column=0, sticky=(N, E, W))
    subframe.grid(row=1, column=0, sticky=(N, S, E, W))
    input_frame.grid(row=0, column=0, sticky=(N, E, W))
    discovery_datetime_label.grid(row=0, column=0, sticky=E)
    self.discovery_datetime_entry.grid(row=0, column=1, sticky=W)
    contained_datetime_label.grid(row=1, column=0, sticky=E)
    self.contained_datetime_entry.grid(row=1, column=1, sticky=W)
    fire_size_label.grid(row=0, column=2, sticky=E)
    self.fire_size_entry.grid(row=0, column=3, sticky=W)
    location_input_frame.grid(row=2, column=0, rowspan=4, columnspan=4, sticky=EW)
    state_label.grid(row=0, column=0, sticky=E)
    self.state_entry.grid(row=0, column=1, sticky=W)
    county_label.grid(row=1, column=0, sticky=E)
    self.county_entry.grid(row=1, column=1, sticky=W)
    location_separator.grid(row=0, column=2, rowspan=2, sticky=NS)
    longitude_label.grid(row=0, column=3, sticky=E)
    self.longitude_entry.grid(row=0, column=4, sticky=W)
    latitude_label.grid(row=1, column=3, sticky=E)
    self.latitude_entry.grid(row=1, column=4, sticky=W)

    # Configure the grid
    self.rowconfigure((0,), weight=1)
    self.rowconfigure((1,), weight=10)
    self.columnconfigure((0,), weight=1)
    subframe.rowconfigure((0,), weight=1)
    subframe.columnconfigure((0,), weight=1)
    input_frame.rowconfigure((0, 1, 2, 3), weight=1)
    input_frame.columnconfigure((0, 1, 2, 3), weight=1)
    location_input_frame.rowconfigure((0, 1), weight=1)
    location_input_frame.columnconfigure((0, 1, 3, 4), weight=5)
    location_input_frame.columnconfigure((2,), weight=1)

  def set_up_state_county_variables(self):
    self.fips_codes_df = get_fips_codes_dataframe()
    state_names = sorted(self.fips_codes_df.state_name.unique())
    self.state_names_county_names_combined_fips_codes = { '-----': None }
    for state_name in state_names:
      self.state_names_county_names_combined_fips_codes[state_name] = {}
      for _, values in self.fips_codes_df[self.fips_codes_df.state_name == state_name].iterrows():
        county_name, state_code, county_code = values.county_name, values.state_numeric_code, values.county_numeric_code
        self.state_names_county_names_combined_fips_codes[state_name][county_name] = state_code + county_code

  def state_names(self):
    return tuple(self.state_names_county_names_combined_fips_codes.keys())

  def county_names(self, state_name):
    try:
      return tuple(self.state_names_county_names_combined_fips_codes[state_name].keys())
    except: pass

  def handle_state_selected(self, *_):
    state_name = self.state_var.get()
    print(state_name)
    county_names = self.county_names(state_name)
    if county_names:
      self.county_entry.configure(state=NORMAL, values=county_names)
      self.county_entry.current(0)
    else:
      self.county_entry.configure(state=DISABLED, values=())
      self.county_entry.set('')
