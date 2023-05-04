import ast
from processors.call_processors import CallProcessor

code = 'import pandas\nx=foo(a=5, b=1)\ndf = pandas.read_csv("example.csv")\ndf.show(n=10)\ndf.groupby(["a","b","c"]).agg({"a": "count"})\n'
tree = ast.parse(code)

c = CallProcessor()
c.visit(tree)

print(c.calls)

