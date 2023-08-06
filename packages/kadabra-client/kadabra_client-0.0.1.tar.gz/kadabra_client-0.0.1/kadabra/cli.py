import click
import tornado
import streamlit as sl
from streamlit.cli import _get_command_line_as_string
from streamlit.bootstrap import _on_server_start
from streamlit.bootstrap import _fix_matplotlib_crash
from .server.server import Server
from .createapp.standard import StandardLayout
from pathlib import Path
import sys

@click.group()
def main():
  """Use the line below to run your script:

    $ kadabra run your_script.py
  """
  pass

@main.command("start")
def main_start():
  """Run a Python script"""

  main_file = Path('main.py')
  if not main_file.exists():
    print(f"Could not find required file: {main_file}")
    sys.exit()

  _fix_matplotlib_crash()
  ioloop = tornado.ioloop.IOLoop.current()
  command_line = _get_command_line_as_string()
  sl._is_running_with_streamlit = True
  server = Server(ioloop, str(main_file.resolve()), command_line)
  server.start(_on_server_start)
  ioloop.start()

@main.command("new")
@click.argument("project-directory", required=True)
def main_new(project_directory):
  """Creates an empty data script"""
  layout = StandardLayout(project_directory)
  layout.create()

if __name__ == "__main__":
  main()