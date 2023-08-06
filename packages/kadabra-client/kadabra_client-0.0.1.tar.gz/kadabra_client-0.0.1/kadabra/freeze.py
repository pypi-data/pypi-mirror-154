import sys
from IPython import get_ipython
from IPython.core.magic import (
  Magics,
  cell_magic,
  magics_class,
)
from IPython.core import magic_arguments
from pathlib import Path
from os import linesep

from click import UsageError

from .decouple.dependency import get_packages
from .createapp.layout import Layout
from .status import Status
from .lint import resolveUndefined
from .decouple.injector import AbstractFileSystem, Injector

class DelayedWriter(AbstractFileSystem):
  def __init__(self):
    self._tasks = []

  def put(self, name, relpath, content):
    def putdata(dir):
      path = dir / relpath
      with Status(f"Writing '{name}' at {path}'"):
        with path.open('wb') as f:
          f.write(content)
    self._tasks.append(putdata)

  def write(self, projectdir):
    for task in self._tasks:
      task(projectdir)

@magics_class
class FreezeMagic(Magics):
  def __init__(self, shell):
    Magics.__init__(self, shell=shell)

  @magic_arguments.magic_arguments()
  @magic_arguments.argument('path',
    help="The path to create the frozen cell at."
  )
  @cell_magic("freeze")
  def cmagic(self, line="", cell=""):
    args = magic_arguments.parse_argstring(self.cmagic, line)
    self.freeze(cell, Path(args.path))
  
  def freeze(self, cell, projectdir):
    try:
      undefs = resolveUndefined(cell)
    except Exception as e:
      print(e, file=sys.stderr)
      return
    varnames = sorted(list(set([u.message_args[0] for u in undefs])))
    
    sourceWriter = DelayedWriter()
    injector = Injector(sourceWriter)
    with injector.addVariables() as add:
      for varname in varnames:
        try:
          obj = self.shell.user_ns[varname]
        except KeyError:
          print(f"Dependency '{varname}' is not defined", file=sys.stderr)
          return
        try:
          add(varname, obj)
        except Exception as err:
          print(f"Could not serialize or inject {varname}: {err}", file=sys.stderr)
          return
  
    main_path = projectdir / "main.py"
    sep = linesep if len(injector.code) > 0 else ""
    code = injector.code + sep + cell

    layout = Layout(projectdir, get_packages(code))
    layout.create()
    (projectdir / injector.dataDir).mkdir(parents=True, exist_ok=True)
    sourceWriter.write(projectdir)
    with Status(f"Writing cell at {main_path}"):
      with main_path.open('w', encoding='utf-8') as f:
        f.write(code)

get_ipython().register_magics(FreezeMagic)
