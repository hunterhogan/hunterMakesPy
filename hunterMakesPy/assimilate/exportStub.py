# ruff: noqa: D100
from astToolkit import Be, dump, Grab, Make, NodeChanger, parseLogicalPath2astModule, Then
from astToolkit.transformationTools import write_astModule
import ast

astModule = parseLogicalPath2astModule('humpy_toolz.dicttoolz')

NodeChanger(Be.FunctionDef, Grab.bodyAttribute(Then.replaceWith([Make.Constant(...)]))
).visit(astModule)

print(ast.unparse(astModule))
