import ast
from importlib_metadata import packages_distributions, version

class Visitor(ast.NodeVisitor):
  def __init__(self):
    self.imports = set()
  
  def visit_Import(self, node):
    self._visit_import_stmt(node, "")

  def visit_ImportFrom(self, node):
    if node.level == 0:
      abs_module = node.module
      self._visit_import_stmt(node, abs_module + ".")
  
  def _visit_import_stmt(self, node, import_prefix):
    for alias in node.names:
      self.imports.add(import_prefix + alias.name)

def get_imports(code):
  tree = ast.parse(code)
  visitor = Visitor()
  visitor.visit(tree)
  return sorted(visitor.imports)

def get_packages(code):
  deps = set()
  packages = packages_distributions()
  for symbol in get_imports(code):
    mod = symbol.split('.')[0]
    if mod in packages:
      if len(packages[mod]) == 1:
        pkg = packages[mod][0]
        deps.add((mod, version(pkg)))
  return sorted(deps, key=lambda x: x[0])
