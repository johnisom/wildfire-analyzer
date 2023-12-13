from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from .custom_widgets import NotebookFrame, Title, Subtitle, DefaultEntry, DatetimeEntry
from ..location_info import get_fips_codes_dataframe, are_coordinates_inside_usa
from ..prediction import run_fips_model_prediction, run_lonlat_model_prediction
from ..bindings import plot_lonlat_confusion_matrix, plot_fipscode_confusion_matrix
import datetime

class PredictionsFrame(NotebookFrame):
  title = 'Predictions'
  max_year = 2015
  min_year = 1992

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
    subframe = ttk.LabelFrame(self, text='Predict cause of fire by giving some parameters', padding=5)

    input_frame = ttk.Frame(subframe)
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
    predict_button = ttk.Button(input_frame, text='Predict fire cause', command=self.run_prediction)
    display_frame = ttk.LabelFrame(subframe, padding=5, text='Predicted Category Results')
    predicted_category_label = ttk.Label(display_frame, text='Top predicted category:')
    self.predicted_category_var = StringVar()
    predicted_category = ttk.Label(display_frame, textvariable=self.predicted_category_var, font=('Helvetica', 12))
    probabilities_frame = ttk.Frame(display_frame)
    probabilities_label = ttk.Label(probabilities_frame, text='Top 3 predicted categories and relative probabilities:')
    probability_1_label = ttk.Label(probabilities_frame, text='1. ')
    self.probability_1_cause_var = StringVar()
    probability_1_cause = ttk.Label(probabilities_frame, textvariable=self.probability_1_cause_var)
    probability_1_colon_label = ttk.Label(probabilities_frame, text=':')
    self.probability_1_percent_var = StringVar()
    probability_1_percent = ttk.Label(probabilities_frame, textvariable=self.probability_1_percent_var)
    probability_1_percent_label = ttk.Label(probabilities_frame, text='%')
    probability_2_label = ttk.Label(probabilities_frame, text='2. ')
    self.probability_2_cause_var = StringVar()
    probability_2_cause = ttk.Label(probabilities_frame, textvariable=self.probability_2_cause_var)
    probability_2_colon_label = ttk.Label(probabilities_frame, text=':')
    self.probability_2_percent_var = StringVar()
    probability_2_percent = ttk.Label(probabilities_frame, textvariable=self.probability_2_percent_var)
    probability_2_percent_label = ttk.Label(probabilities_frame, text='%')
    probability_3_label = ttk.Label(probabilities_frame, text='3. ')
    self.probability_3_cause_var = StringVar()
    probability_3_cause = ttk.Label(probabilities_frame, textvariable=self.probability_3_cause_var)
    probability_3_colon_label = ttk.Label(probabilities_frame, text=':')
    self.probability_3_percent_var = StringVar()
    probability_3_percent = ttk.Label(probabilities_frame, textvariable=self.probability_3_percent_var)
    probability_3_percent_label = ttk.Label(probabilities_frame, text='%')
    confusion_matrix_buttons_frame = ttk.LabelFrame(subframe, text="ML Models' Confusion Matrices")
    fips_confusion_matrix_button = ttk.Button(confusion_matrix_buttons_frame, text='State/County Model', command=self.show_fips_confusion_matrix)
    lonlat_confusion_matrix_button = ttk.Button(confusion_matrix_buttons_frame, text='Longitude/Latitude Model', command=self.show_lonlat_confusion_matrix)

    # Set items on the grid
    title.grid(row=0, column=0, sticky=(N, E, W))
    subframe.grid(row=1, column=0, sticky=NSEW)
    input_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)
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
    predict_button.grid(row=6, column=0, columnspan=4, pady=5, sticky=NSEW)
    display_frame.grid(row=1, column=0, sticky=NSEW)
    predicted_category_label.grid(row=0, column=0, sticky=E)
    predicted_category.grid(row=0, column=1, sticky=W)
    probabilities_frame.grid(row=1, column=0, rowspan=2, columnspan=3, sticky=NSEW)
    probabilities_label.grid(row=0, column=0, columnspan=5, sticky=(N, E, W))
    probability_1_label.grid(row=1, column=0, sticky=E)
    probability_1_cause.grid(row=1, column=1, sticky=E)
    probability_1_colon_label.grid(row=1, column=2)
    probability_1_percent.grid(row=1, column=3, sticky=W)
    probability_1_percent_label.grid(row=1, column=4, sticky=W)
    probability_2_label.grid(row=2, column=0, sticky=E)
    probability_2_cause.grid(row=2, column=1, sticky=E)
    probability_2_colon_label.grid(row=2, column=2)
    probability_2_percent.grid(row=2, column=3, sticky=W)
    probability_2_percent_label.grid(row=2, column=4, sticky=W)
    probability_3_label.grid(row=3, column=0, sticky=E)
    probability_3_cause.grid(row=3, column=1, sticky=E)
    probability_3_colon_label.grid(row=3, column=2)
    probability_3_percent.grid(row=3, column=3, sticky=W)
    probability_3_percent_label.grid(row=3, column=4, sticky=W)
    confusion_matrix_buttons_frame.grid(row=1, column=1, sticky=NSEW)
    fips_confusion_matrix_button.grid(row=0, column=0, sticky=NSEW, padx=4, pady=4)
    lonlat_confusion_matrix_button.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)

    # Configure the grid
    self.rowconfigure((0,), weight=1)
    self.rowconfigure((1,), weight=5)
    self.columnconfigure((0,), weight=1)
    subframe.rowconfigure((0,), weight=2)
    subframe.rowconfigure((1,), weight=1)
    subframe.columnconfigure((0,), weight=2)
    subframe.columnconfigure((1,), weight=1)
    input_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    input_frame.rowconfigure((6,), weight=2)
    input_frame.columnconfigure((0, 1, 2, 3), weight=1)
    location_input_frame.rowconfigure((0, 1), weight=1)
    location_input_frame.columnconfigure((0, 1, 3, 4), weight=5)
    location_input_frame.columnconfigure((2,), weight=1)
    display_frame.rowconfigure((0,), weight=2)
    display_frame.rowconfigure((1, 2), weight=1)
    display_frame.columnconfigure((0, 1), weight=1)
    display_frame.columnconfigure((2,), weight=2)
    probabilities_frame.rowconfigure((0,), weight=3)
    probabilities_frame.rowconfigure((1, 2, 3), weight=2)
    probabilities_frame.columnconfigure((0, 2, 3, 4), weight=1)
    probabilities_frame.columnconfigure((1), weight=2)
    confusion_matrix_buttons_frame.rowconfigure((0, 1), weight=1)
    confusion_matrix_buttons_frame.columnconfigure((0,), weight=1)

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

  def get_fips_code(self, state_name='', county_name=''):
    fips_entry = self.fips_codes_df[(self.fips_codes_df.state_name == state_name) & (self.fips_codes_df.county_name == county_name)].iloc[0]
    return fips_entry.state_numeric_code + fips_entry.county_numeric_code

  def handle_state_selected(self, *_):
    state_name = self.state_var.get()
    county_names = self.county_names(state_name)
    if county_names:
      self.county_entry.configure(state=NORMAL, values=county_names)
      self.county_entry.current(0)
    else:
      self.county_entry.configure(state=DISABLED, values=())
      self.county_entry.set('')

  def collect_inputs(self):
    kwargs = {
      'discovery_datetime': self.discovery_datetime_entry.get_datetime(),
      'contained_datetime': self.contained_datetime_entry.get_datetime(),
      'fire_size': 0.0,
    }
    if self.fire_size_entry.get_value() != '':
      kwargs['fire_size'] = float(self.fire_size_entry.get_value())
    if self.longitude_entry.get_value() != '':
      kwargs['longitude'] = float(self.longitude_entry.get_value())
    if self.latitude_entry.get_value() != '':
      kwargs['latitude'] = float(self.latitude_entry.get_value())
    if self.state_var.get() != '-----' and self.county_var.get() != '':
      kwargs['combined_fips_code'] = self.get_fips_code(state_name=self.state_var.get(), county_name=self.county_var.get())

    return kwargs

  def validate_inputs(self, kwargs):
    msgs = []
    # Check datetime validities
    if type(kwargs['discovery_datetime']) != datetime.datetime:
      msgs.append('Discovery datetime invalid.')
    if type(kwargs['contained_datetime']) != datetime.datetime:
      msgs.append('Contained datetime invalid.')
    if len(msgs) == 0 and kwargs['contained_datetime'] <= kwargs['discovery_datetime']:
      msgs.append('Discovery datetime must be earlier than Contained datetime.')
    # Check firesize is positive
    if kwargs['fire_size'] <= 0:
      msgs.append('Fire size must be positive and non-zero.')
    # Check location
    longitude = kwargs.get('longitude')
    latitude = kwargs.get('latitude')
    if (longitude is not None or latitude is not None) and kwargs.get('combined_fips_code') is not None:
      msgs.append('Location must be either by State/County or by Longitude/Latitude, NOT both.')
    elif longitude is None and latitude is None and kwargs.get('combined_fips_code') is None:
      msgs.append('Location must be provided, either by State/County or Longitude/Latitude.')
    elif longitude is not None and latitude is None:
      msgs.append('Latitude must be provided.')
    elif longitude is None and latitude is not None:
      msgs.append('Longitude must be provided.')
    # Check if longitude and latitude are within bounds
    if longitude is not None and latitude is not None and not are_coordinates_inside_usa(float(longitude), float(latitude)):
      msgs.append('Longitude and Latitude are not within the boundaries of any USA State or DC or Puerto Rico.')
    return msgs

  def run_prediction(self):
    kwargs = self.collect_inputs()
    err_msgs = self.validate_inputs(kwargs)
    if len(err_msgs) > 0:
      showerror(parent=self, title='Please fix the following errors', message='\n'.join(err_msgs))
      return
    if kwargs.get('combined_fips_code') is not None:
      predicted_category_probabilities = run_fips_model_prediction(**kwargs)
    else:
      predicted_category_probabilities = run_lonlat_model_prediction(**kwargs)
    self.display_predicted_info(predicted_category_probabilities)

  def display_predicted_info(self, probabilities):
    self.predicted_category_var.set(probabilities[0][0])
    self.probability_1_cause_var.set(probabilities[0][0])
    self.probability_2_cause_var.set(probabilities[1][0])
    self.probability_3_cause_var.set(probabilities[2][0])
    self.probability_1_percent_var.set(f'{probabilities[0][1] * 100:.2f}')
    self.probability_2_percent_var.set(f'{probabilities[1][1] * 100:.2f}')
    self.probability_3_percent_var.set(f'{probabilities[2][1] * 100:.2f}')

  def show_fips_confusion_matrix(self):
    plot_lonlat_confusion_matrix()

  def show_lonlat_confusion_matrix(self):
    plot_fipscode_confusion_matrix()
