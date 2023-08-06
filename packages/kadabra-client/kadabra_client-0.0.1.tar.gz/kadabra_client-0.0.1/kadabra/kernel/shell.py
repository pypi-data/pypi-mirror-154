from io import BytesIO
from streamlit import _main as slDg
from IPython.core.interactiveshell import InteractiveShell
import sys
from PIL import Image
from base64 import b64encode, b64decode
from importlib import import_module

class StWriter:
  def write(self, str):
    slDg.write(str)
  def flush(self):
    pass

class DisplayPublisher:
  def publish(self, data, metadata=None, source=None, *, transient=None, update=False):
    img_mimes = ['image/bmp', 'image/png', 'image/jpeg', 'image/gif']
    if 'text/html' in data:
      slDg.markdown(data['text/html'], unsafe_allow_html=True)
    elif 'text/markdown' in data:
      slDg.markdown(data['text/markdown'])
    elif 'text/latex' in data:
      slDg.latex(data['text/latex'])
    elif 'image/svg+xml' in data:
      svg = data['image/svg+xml']
      b64 = b64encode(svg.encode('utf-8')).decode("utf-8")
      html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
      slDg.markdown.write(html, unsafe_allow_html=True)
    elif any([m in data for m in img_mimes]):
      d = next(data[m] for m in img_mimes if m in data)
      image = Image.open(BytesIO(b64decode(d)))
      slDg.image(image)
    elif 'text/plain' in data:
      slDg.write(data['text/plain'])

class DisplayHook(object):
  def __call__(self, result=None):
    if result is None:
      return
    slDg.write(result)

class capture_output(object):
  def __enter__(self):
    from IPython.core.getipython import get_ipython

    self.sys_stdout = sys.stdout
    self.sys_stderr = sys.stderr

    self.shell = get_ipython()
    assert self.shell is not None

    sys.stdout = StWriter()
    sys.stderr = StWriter()

    self.save_display_pub = self.shell.display_pub
    self.shell.display_pub = DisplayPublisher()
    self.save_display_hook = sys.displayhook
    sys.displayhook = DisplayHook()
  
  def __exit__(self, exc_type, exc_value, traceback):
    sys.stdout = self.sys_stdout
    sys.stderr = self.sys_stderr
    self.shell.display_pub = self.save_display_pub
    sys.displayhook = self.save_display_hook

# Copied from IPython.core.display_functions
def shell_display(
  *objs,
  clear=False,
  **kwargs
):
  from IPython.core.display import display as ipDisplay
  to_display = []
  for obj in objs:
    handled = False
    try:
      mpl = import_module('matplotlib')
      if isinstance(obj, mpl.figure.Figure):
        slDg.pyplot(obj, clear_figure=clear)
        handled = True
    except ModuleNotFoundError:
      pass
    try:
      pd = import_module('pandas')
      if isinstance(obj, pd.DataFrame):
        slDg.write(obj)
        handled = True
    except ModuleNotFoundError:
      pass
    if not handled:
      to_display.append(obj)
  if len(to_display) > 0:
    return ipDisplay(*to_display, clear=clear, **kwargs)

class Shell(InteractiveShell):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.setup()
  
  def enable_gui(self, gui=None):
    # see TerminalInteractiveShell
    self.active_eventloop = self._inputhook = None

  def setup(self):
    try:
      # Monkey-patching display to intercept supported objects
      import IPython.display
      IPython.display.display = shell_display

      mpl = import_module('matplotlib')
      mpl.rcParams.update(mpl.rcParamsOrig)
      self.enable_pylab(gui='inline')
    except ModuleNotFoundError:
      pass

  def run_cell(self, code):
    with self.display_trap:
      """
        see IPython.core.display_trap __enter__ logic

        %%capture magic works because interactiveshell does not set the default displaytrap
        on nested "self.display_trap" calls

        Without this, the default display_trap captures the output instead of the
        CapturingDisplayHook that's set with capture_output below

        Finding this out is a debugging nightmare as is finding anything related to the display_hook
        not set properly. That's because pdb overwrites sys.display_hook.
      """

      with capture_output():
        return super().run_cell(code)
  
  def _showtraceback(self, etype, evalue, stb):
    """Exceptions are handled with run_cell return value"""
    pass
