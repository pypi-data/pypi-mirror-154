from .layout import Layout

DEFAULT = u'print("Hello, World!")'

class StandardLayout(Layout):
  def _create_default(self):
    main = self.path / "main.py"
    with main.open("w", encoding="utf-8") as f:
        f.write(DEFAULT)
