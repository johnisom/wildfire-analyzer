from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from .custom_widgets import NotebookFrame, DefaultEntry
from ..state_and_county_info import REGIONS_STATE_ALPHA_CODES, STATE_ALPHA_FIPS_CODES
from ..bindings import plot_fire_cause_counts, plot_fire_cause_area_burned, plot_fire_county_counts, plot_fire_county_area_burned, plot_everything

class PlotsFrame(NotebookFrame):
  title = 'Plots'
  max_year = 2015
  min_year = 1992

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    title_label = ttk.Label(self, text='Plots')

    form_frame = ttk.LabelFrame(self, text='Select Area to Plot: One or more regions and/or one more more comma-separated states')

    checkbutton_frame = ttk.Frame(form_frame, padding=5)
    checkbutton_label = ttk.Label(checkbutton_frame, text='Region')
    self.checkbuttons = {}
    for region in REGIONS_STATE_ALPHA_CODES.keys():
      checked = BooleanVar(value=False)
      checkbutton = ttk.Checkbutton(checkbutton_frame, text=region.title(), variable=checked, onvalue=True, offvalue=False)
      self.checkbuttons[region] = (checkbutton, checked)
    self.checkbuttons['lower48'][1].set(True)

    state_entry_frame = ttk.Frame(form_frame, padding=5)
    state_entry_label = ttk.Label(state_entry_frame, text='State alpha codes')
    self.state_entry_var = StringVar()
    self.state_entry = DefaultEntry(state_entry_frame,  default_text='AL, KY, UT, etc.', textvariable=self.state_entry_var)

    years_entry_frame = ttk.Frame(form_frame, padding=5)
    years_entry_label = ttk.Label(years_entry_frame, text='Enter start and end year (inclusive) to filter visualized data.')
    start_year_label = ttk.Label(years_entry_frame, text='Start year:')
    self.start_year_variable = StringVar()
    self.start_year_entry = DefaultEntry(years_entry_frame, default_text=str(self.min_year), textvariable=self.start_year_variable)
    end_year_label = ttk.Label(years_entry_frame, text='End year:')
    self.end_year_variable = StringVar()
    self.end_year_entry = DefaultEntry(years_entry_frame, default_text=str(self.max_year), textvariable=self.end_year_variable)

    submit_frame = ttk.Frame(form_frame)
    self.fire_cause_counts_button = ttk.Button(submit_frame, text='# Fires by Cause', command=lambda *e: self.handle_button(button_name='fire_cause_counts'))
    self.fire_cause_area_button = ttk.Button(submit_frame, text='Area Burned by Cause', command=lambda *e: self.handle_button(button_name='fire_cause_area'))
    self.county_counts_button = ttk.Button(submit_frame, text='# Fires by County', command=lambda *e: self.handle_button(button_name='county_counts'))
    self.county_area_button = ttk.Button(submit_frame, text='Area Burned by County', command=lambda *e: self.handle_button(button_name='county_area'))
    self.all_button = ttk.Button(submit_frame, text='All Charts', command=lambda *e: self.handle_button(button_name='all'))

    # Set up the grid
    title_label.grid(row=0, column=0, columnspan=3, sticky=EW)
    form_frame.grid(row=1, column=0, sticky=NSEW)
    checkbutton_frame.grid(row=0, column=0, rowspan=2, sticky=NW)
    checkbutton_label.grid(row=0, column=0, sticky=(N, E, W))
    for i, (checkbutton, _) in enumerate(self.checkbuttons.values()):
      checkbutton.grid(row=i + 1, column=0, sticky=EW)
    state_entry_frame.grid(row=0, column=1, sticky=N)
    state_entry_label.grid(row=0, column=0, sticky=EW)
    self.state_entry.grid(row=1, column=0, sticky=EW)
    years_entry_frame.grid(row=1, column=1, sticky=N)
    years_entry_label.grid(row=0, column=0, columnspan=4)
    start_year_label.grid(row=1, column=0)
    self.start_year_entry.grid(row=1, column=1)
    end_year_label.grid(row=1, column=2)
    self.end_year_entry.grid(row=1, column=3)
    submit_frame.grid(row=2, column=0, columnspan=2, sticky=NSEW)
    self.fire_cause_counts_button.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
    self.fire_cause_area_button.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
    self.county_counts_button.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
    self.county_area_button.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
    self.all_button.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

    # Configure the Grid (optional)
    self.rowconfigure((0,), weight=1)
    self.rowconfigure((1,), weight=10)
    self.columnconfigure((0,), weight=1)
    form_frame.rowconfigure((0, 1), weight=5)
    form_frame.rowconfigure((2,), weight=1)
    form_frame.columnconfigure((0, 1), weight=1)
    checkbutton_frame.rowconfigure(tuple(range(len(self.checkbuttons) + 1)), weight=1)
    checkbutton_frame.columnconfigure((0,), weight=1)
    state_entry_frame.rowconfigure((0, 1), weight=1)
    state_entry_frame.columnconfigure((0,), weight=1)
    years_entry_frame.rowconfigure((0, 1), weight=1)
    years_entry_frame.columnconfigure((0, 1, 2, 3), weight=1)
    submit_frame.rowconfigure((0,), weight=1)
    submit_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

  def handle_button(self, button_name):
    kwargs = self.collect_inputs()
    err_msgs = self.validate_inputs(kwargs)
    if len(err_msgs) > 0:
      showerror(title='Please fix the following errors', message='\n'.join(err_msgs))
      return

  def collect_inputs(self):
    kwargs = {
      'keys': set()
    }

    for region, (_, checkedvar) in self.checkbuttons.items():
      if checkedvar.get():
        kwargs['keys'].add(region)

    alpha_codes = self.state_entry.get_value()
    if alpha_codes != '':
      for code in alpha_codes.replace(' ', '').split(','):
        if len(code) == 2:
          kwargs['keys'].add(code)

    start_year = self.start_year_entry.get_value()
    if start_year != '':
      kwargs['year_start'] = int(start_year)
    end_year = self.end_year_entry.get_value()
    if end_year != '':
      kwargs['year_end'] = int(end_year)

    return kwargs

  def validate_inputs(self, kwargs):
    msgs = []

    # validate keys
    if len(kwargs['keys']) == 0:
      msgs.append('Must select at least 1 region or enter 1 two-letter state code.')
    for key in kwargs['keys']:
      if len(key) == 2 and key not in STATE_ALPHA_FIPS_CODES:
        msgs.append(f'{key!r} not a valid two-letter state code.')

    # validate years
    if type(kwargs.get('year_start')) == int and type(kwargs.get('year_end')) == int and kwargs.get('year_start') > kwargs.get('year_end'):
      msgs.append('Start year must be less than or equal to end year.')
    if type(kwargs.get('year_start')) == int and kwargs.get('year_start') < self.min_year:
      msgs.append(f'Start year must be greater than or equal to min year ({self.min_year}).')
    if type(kwargs.get('year_end')) == int and kwargs.get('year_end') > self.max_year:
      msgs.append(f'End year must be less than or equal to max year ({self.max_year}).')
    if type(kwargs.get('year_end')) == int and kwargs.get('year_end') < self.min_year:
      msgs.append(f'End year must be greater than or equal to min year ({self.min_year}).')
    if type(kwargs.get('year_start')) == int and kwargs.get('year_start') > self.max_year:
      msgs.append(f'Start year must be less than or equal to max year ({self.max_year}).')

    return msgs
