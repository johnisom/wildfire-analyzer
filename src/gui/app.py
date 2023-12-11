from tkinter import *
from tkinter.messagebox import showwarning
from tkinter import ttk
from .welcome import WelcomeFrame
from .plots import PlotsFrame
from .predictions import PredictionsFrame
from .credits import CreditsFrame, LicenseFrame
from ..prediction import FIPS_ENCODER_PATH, FIPS_MODEL_PATH, LONLAT_MODEL_PATH
from .custom_widgets import Title

class App(Tk):
  def __init__(self, enable_predictions=True, **kwargs):
    super().__init__(**kwargs)

    self.title('Wildfire Analyzer')
    self.resizable(False, False)
    self.geometry('650x400')

    # Set up the notebook and the frames in the notebook
    notebook = ttk.Notebook(self, padding=2)
    welcome_frame = WelcomeFrame(notebook)
    plots_frame = PlotsFrame(notebook)
    credits_frame = CreditsFrame(notebook)
    license_frame = LicenseFrame(notebook)
    notebook.add(welcome_frame, text=welcome_frame.title)
    notebook.add(plots_frame, text=plots_frame.title)
    if enable_predictions:
      predictions_frame = PredictionsFrame(notebook)
      notebook.add(predictions_frame, text=predictions_frame.title)
    else:
      no_ml_message = 'The "joblib-objects" directory was unable to be found, or the files within don\'t match the registered name for the predictive models.\n' \
        'To remedy this, unzip the "joblib-objects.zip" archive into a new directory called "joblib-objects".\n' \
        'Ensure the following files are present in the application:\n' \
        f'- {FIPS_MODEL_PATH}\n' \
        f'- {FIPS_ENCODER_PATH}\n' \
        f'- {LONLAT_MODEL_PATH}\n\n' \
        'The application will continue, but the "Predictions" feature is disabled.'
      self.warn(title='Unable to load ML predictive models!', message=no_ml_message)
    notebook.add(credits_frame, text=credits_frame.title)
    notebook.add(license_frame, text=license_frame.title)

    # Set up the grid
    notebook.grid(row=0, column=0, sticky=NSEW)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

  def warn(self, title='', message=''):
    self.warn_window = Toplevel(self)
    self.warn_window.title(title)
    Title(self.warn_window, text=title).pack()
    ttk.Label(self.warn_window, text=message).pack()
    ttk.Button(self.warn_window, text='OK', command=self.unwarn).pack()
    self.warn_window.protocol('WM_DELETE_WINDOW', self.unwarn)
    self.disable()

  def unwarn(self):
    self.enable()
    self.warn_window.destroy()

  def disable(self):
    self.warn_window.grab_set()
    self.withdraw()

  def enable(self):
    self.deiconify()
    self.warn_window.grab_release()
