from astor import to_source
import ast
from pickle import (
  _Unpickler, _Stop, UnpicklingError,
  PROTO, FRAME, SHORT_BINUNICODE, MEMOIZE, STACK_GLOBAL, STOP, TUPLE1, REDUCE
)
from io import BytesIO, StringIO
from collections import defaultdict
from contextlib import contextmanager
from streamlit.type_util import is_type, _PANDAS_DF_TYPE_STR, _PANDAS_SERIES_TYPE_STR
from pathlib import Path
import cloudpickle

class AbstractFileSystem:
  def put(self, name, path, content):
    raise NotImplementedError

class RewriteName(ast.NodeTransformer):
  def __init__(self, oldId, newId):
    self.oldId = oldId
    self.newId = newId
  def visit_Name(self, node):
    if node.id == self.oldId:
      node.id = self.newId
    return node

class RewriteConstant(ast.NodeTransformer):
  def __init__(self, oldValue, newValue):
    self.oldValue = oldValue
    self.newValue = newValue
  def visit_Constant(self, node):
    if node.value == self.oldValue:
      node.value = self.newValue
    return node

class CodeUnpickler(_Unpickler):
  def __init__(self, file, asname):
    super().__init__(file)
    self.asname = asname

  def find_class(self, module, name):
    if self.proto >= 4:
      if module == 'cloudpickle.cloudpickle' and name == 'subimport':
        return ast.Import(type_ignores=[])
      else:
        asname = self.asname if name != self.asname else None
        return ast.ImportFrom(module=module, names=[ast.alias(name=name, asname=asname)], level=0)
    else:
      raise UnpicklingError("Not supported")

  def load_default(self):
    raise UnpicklingError("Not supported")

  def load_stop(self):
    value = self.stack.pop()
    if isinstance(value, ast.AST):
      raise _Stop(value)
    else:
      raise UnpicklingError("Not supported")
  
  def load_reduce(self):
    stack = self.stack
    args = stack.pop()
    imp = stack[-1]
    if isinstance(imp, ast.Import) and len(args) == 1:
      name = args[0]
      asname = self.asname if name != self.asname else None
      imp.names = [ast.alias(name=name, asname=asname)]
    else:
      raise UnpicklingError("Not supported")

  dispatch = defaultdict(lambda: CodeUnpickler.load_default)
  dispatch[PROTO[0]] = _Unpickler.load_proto
  dispatch[FRAME[0]] = _Unpickler.load_frame
  dispatch[SHORT_BINUNICODE[0]] = _Unpickler.load_short_binunicode
  dispatch[MEMOIZE[0]] = _Unpickler.load_memoize
  dispatch[STACK_GLOBAL[0]] = _Unpickler.load_stack_global
  dispatch[TUPLE1[0]] = _Unpickler.load_tuple1
  dispatch[STOP[0]] = load_stop
  dispatch[REDUCE[0]] = load_reduce
  
class Injector:
  def __init__(self, fs):
    self.fs = fs
    self.dataDir = Path('data')
    self._imports = []
    self._statements = []
    self._moduleStatements = []
    self._modules = dict()
  
  def appendStatement(self, stmt):
    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
      self._imports.append(stmt)
      if isinstance(stmt, ast.Import):
        self._modules[stmt.names[0].name] = stmt.names[0].asname or stmt.names[0].name
    else:
      self._statements.append(stmt)
  
  def appendAfterModuleStatement(self, mod, fn):
    self._moduleStatements.append((mod, fn))
  
  @contextmanager
  def addVariables(self):
    yield self.add
    for (mod, fn) in self._moduleStatements:
      if mod not in self._modules:
        self.appendStatement(ast.Import(names=[ast.alias(name=mod, asname=None)]))
      self.appendStatement(fn(self._modules[mod]))

  def add(self, name, obj):
    if isinstance(obj, (int, float, bool, str)):
      self.add_inline(name, obj)
    elif is_type(obj, _PANDAS_DF_TYPE_STR):
      self.add_read_dataframe(name, obj)
    elif is_type(obj, _PANDAS_SERIES_TYPE_STR):
      self.add_read_series(name, obj)
    else:
      buff = BytesIO(); cloudpickle.dump(obj, buff)
      try:
        self.add_inline_pickle(name, buff)
        return
      except UnpicklingError:
        pass
      self.add_read_pickle(name, buff.getvalue())
  
  def add_inline(self, name, obj):
    stmt = ast.parse('myvar = 123').body[0]
    stmt = RewriteName('myvar', name).visit(RewriteConstant(123, obj).visit(stmt))
    self.appendStatement(stmt)
  
  def add_read_dataframe(self, name, obj):
    path = self.dataDir / f'{name}.json'
    content = StringIO(); obj.to_json(content, orient="table"); content = content.getvalue().encode('utf-8')
    self.fs.put(name, path, content)
    stmt = ast.parse('myvar = mypandas.read_json("mypath", orient="table")')
    stmt = RewriteConstant('mypath', str(path)).visit(stmt)
    stmt = RewriteName('myvar', name).visit(stmt)
    self.appendAfterModuleStatement("pandas", lambda pd: 
      RewriteName('mypandas', pd).visit(stmt))
  
  def add_read_series(self, name, obj):
    path = self.dataDir / f'{name}.json'
    content = StringIO(); obj.to_json(content, orient="table"); content = content.getvalue().encode('utf-8')
    self.fs.put(name, path, content)
    stmt = ast.parse('myvar = mypandas.read_json("mypath", orient="table").squeeze()')
    stmt = RewriteConstant('mypath', str(path)).visit(stmt)
    stmt = RewriteName('myvar', name).visit(stmt)
    self.appendAfterModuleStatement("pandas", lambda pd: 
      RewriteName('mypandas', pd).visit(stmt))
  
  def add_inline_pickle(self, name, buffer):
    buffer.seek(0)
    stmt = CodeUnpickler(buffer, name).load()
    self.appendStatement(stmt)

  def add_read_pickle(self, name, content):
    path = self.dataDir / f'{name}.pickle'
    self.fs.put(name, path, content)
    stmt = ast.parse('myvar = mypickle.load(open("mypath", "rb"))')
    stmt = RewriteConstant('mypath', str(path)).visit(stmt)
    stmt = RewriteName('myvar', name).visit(stmt)
    self.appendAfterModuleStatement("pickle", lambda pckl: 
      RewriteName('mypickle', pckl).visit(stmt))

  @property
  def code(self):
    return to_source(ast.Module(body=(self._imports + self._statements)))
