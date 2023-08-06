from logging import getLogger
from packaging.version import parse
import requests
import json
from tomlkit import loads, dumps
from pathlib import Path
import sys
from typing import Any
from .. import __version__

currentVersion = parse(__version__)

PIPFILE_DEFAULT = """\
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
kadabra_client = "*"

[dev-packages]

[requires]
python_version = ""

[scripts]
start = "kadabra start"
"""

README_DEFAULT = u'''\
# Getting started with Kadabra

This project was bootstrapped with [Kadabra](https://1000words-hq.com).

## Installation

`pipenv install`

## Available scripts

### `pipenv run start`

Run the app and open a browser window to view it.
'''

class Layout(object):

  def __init__(self, projectdir, dependencies=[]):
    self.path = Path(projectdir)
    self.dependencies = dependencies

  @property
  def appName(self) -> str:
    return self.path.name
  
  @property
  def absPath(self) -> str:
    return self.path.resolve()

  def create(self):
    latest = self._fetchLatestVersion()
    if latest is not None and currentVersion < latest:
      print(f"""You are running 'kadabra' {currentVersion}, which is behind the latest release {latest}""")
      print('We recommend always using the latest version of kadabra if possible.')
      sys.exit()
    self._checkAppName()
    self.path.mkdir(parents=True, exist_ok=True)
    self._checkIsSafeToCreateProjectIn()
    print()
    print(f"Creating a new data app in {self.absPath}")
    print()
    self._create_default()
    self._create_readme()
    self._create_pipfile()
    print(f"Success! Created {self.appName} at {self.absPath}")
    print()
    print("Run the app by typing:")
    print("")
    print(f"  cd {self.path}")
    print("  pipenv install")
    print("  pipenv run start")
    print()

  def _fetchLatestVersion(self):
    req = requests.get(f'https://pypi.python.org/pypi/kadabra-client/json')
    version = None
    if req.status_code == requests.codes.ok:
      j = json.loads(req.text.encode('utf-8'))
      releases = j.get('releases', [])
      for release in releases:
        ver = parse(release)
        version = max(version, ver) if version is not None else ver
    return version

  def _checkAppName(self):
    if not (self.appName.isidentifier() and self.appName.islower()):
      print(f"""Cannot create a project named '{self.appName}' because of Python package naming restrictions""")
      print("""\nPlease choose a different project name.""")
      sys.exit()

  def _checkIsSafeToCreateProjectIn(self):
    conflicts = list(self.path.iterdir())
    if len(conflicts) > 0:
      print(f"""The directory {self.path} contains files that would conflict:""")
      for f in conflicts:
        suffix = "/" if (self.path / f).is_dir() else ""
        print(f"  {f}{suffix}")
      print("\nEither try using a new directory name, or remove the files listed above.")
      sys.exit()
  
  def _create_default(self):
    pass
  
  def _create_readme(self):
    readme_file = self.path / "README.md"
    with readme_file.open('w', encoding='utf-8') as f:
      f.write(README_DEFAULT)

  def _create_pipfile(self):
    content = self._generate_pipfile_content()
    pyproj_file = self.path / "Pipfile"
    with pyproj_file.open('w', encoding='utf-8') as f:
      f.write(content)
  
  def _generate_pipfile_content(self):
    content: dict[str, Any] = loads(PIPFILE_DEFAULT)
    content['requires']['python_version'] = '.'.join([str(v) for v in sys.version_info[:2]])
    for (pkg, vers) in self.dependencies:
      content['packages'][pkg] = f'=={vers}'
    return dumps(content)
