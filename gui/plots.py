from tkinter import *
from tkinter import ttk
from .notebook_frame import NotebookFrame
from state_and_county_info import REGIONS_STATE_ALPHA_CODES

class PlotsFrame(NotebookFrame):
  title = 'Plots'

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
    state_entry_frame = ttk.Frame(form_frame, padding=5)
    state_entry_label = ttk.Label(state_entry_frame, text='States (AL, KY, UT, etc.)')
    state_entry = ttk.Entry(state_entry_frame)
    submit_frame = ttk.Frame(form_frame, padding=5)
    self.fire_cause_counts_button = ttk.Button(submit_frame, text='# Fires by Cause', command=lambda *e: self.handle_button(button_name='fire_cause_counts'))
    self.fire_cause_area_button = ttk.Button(submit_frame, text='Area Burned by Cause', command=lambda *e: self.handle_button(button_name='fire_cause_area'))
    self.county_counts_button = ttk.Button(submit_frame, text='# Fires by County', command=lambda *e: self.handle_button(button_name='county_counts'))
    self.county_area_button = ttk.Button(submit_frame, text='Area Burned by County', command=lambda *e: self.handle_button(button_name='county_area'))
    self.all_button = ttk.Button(submit_frame, text='All Charts', command=lambda *e: self.handle_button(button_name='all'))

    # Set up the grid
    title_label.grid(row=0, column=0, columnspan=3, sticky=(E, W))
    form_frame.grid(row=1, column=0, sticky=(N, S, E, W))
    checkbutton_frame.grid(row=0, column=0, sticky=(N, W))
    checkbutton_label.grid(row=0, column=0, sticky=(N, E, W))
    for i, (checkbutton, _) in enumerate(self.checkbuttons.values()):
      checkbutton.grid(row=i + 1, column=0, sticky=(E, W))
    state_entry_frame.grid(row=0, column=1, sticky=(N))
    state_entry_label.grid(row=0, column=0)
    state_entry.grid(row=1, column=0)
    submit_frame.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    self.fire_cause_counts_button.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
    self.fire_cause_area_button.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
    self.county_counts_button.grid(row=0, column=2, sticky=NSEW, padx=5, pady=5)
    self.county_area_button.grid(row=0, column=3, sticky=NSEW, padx=5, pady=5)
    self.all_button.grid(row=0, column=4, sticky=NSEW, padx=5, pady=5)

    self.rowconfigure((0,), weight=1)
    self.rowconfigure((1,), weight=10)
    self.columnconfigure((0,), weight=1)
    form_frame.rowconfigure((0,), weight=5)
    form_frame.rowconfigure((1,), weight=1)
    form_frame.columnconfigure((0, 1), weight=1)
    checkbutton_frame.rowconfigure(tuple(range(len(self.checkbuttons) + 1)), weight=1)
    checkbutton_frame.columnconfigure((0,), weight=1)
    state_entry_frame.rowconfigure((0, 1), weight=1)
    state_entry_frame.columnconfigure((0,), weight=1)
    submit_frame.rowconfigure((0,), weight=1)
    submit_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

  def handle_button(self, button_name):
    print(button_name)
