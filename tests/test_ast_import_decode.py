import ast
import textwrap

from flake8_typing_collections.ast_import_decode import decode

CODE_NOOP = """
import os.path
foo()
def x():
    b.ar()
"""


def test_noop():
    tree = ast.parse(CODE_NOOP)
    node1 = tree.body[1].value.func
    node2 = tree.body[2].body[0].value.func
    name1 = decode(tree, node1)
    name2 = decode(tree, node2)
    assert name1 == "foo"
    assert name2 == "b.ar"


CODE_GLOBAL_IMPORT = """
from collections import defaultdict
import xml.et as et
from os import path as p

defaultdict
et
et.ElementTree
p
"""


def test_global_import():
    tree = ast.parse(CODE_GLOBAL_IMPORT)
    node1 = tree.body[3].value
    node2 = tree.body[4].value
    node3 = tree.body[5].value
    node4 = tree.body[6].value
    name1 = decode(tree, node1)
    name2 = decode(tree, node2)
    name3 = decode(tree, node3)
    name4 = decode(tree, node4)
    assert name1 == "collections.defaultdict"
    assert name2 == "xml.et"
    assert name3 == "xml.et.ElementTree"
    assert name4 == "os.path"


CODE_TRY_IF_WHILE = """
if foo():
    from os import path
else:
    from sys import path

while bar():
    import collections as col

try:
    from typing import List
except Exception:
    from typing import Set
else:
    from typing import Dict
finally:
    from typing import Tuple
    
path
col
List
Set
Dict
Tuple"""


def test_try_if_while():
    tree = ast.parse(CODE_TRY_IF_WHILE)
    node1 = tree.body[3].value
    node2 = tree.body[4].value
    node3 = tree.body[5].value
    node4 = tree.body[6].value
    node5 = tree.body[7].value
    node6 = tree.body[8].value
    name1 = decode(tree, node1)
    name2 = decode(tree, node2)
    name3 = decode(tree, node3)
    name4 = decode(tree, node4)
    name5 = decode(tree, node5)
    name6 = decode(tree, node6)
    assert name1 == "path"
    assert name2 == "col"
    assert name3 == "typing.List"
    assert name4 == "Set"
    assert name5 == "typing.Dict"
    assert name6 == "typing.Tuple"


CODE_ANCESTRY = """
from typing import List

def f():
    from typing import Dict
    
    def g():
        from typing import Union
    
    class H:
        from typing import Tuple
        
        List
        Dict
        Union
        Tuple
        Set

from typing import Set
"""


def test_ancestry():
    tree = ast.parse(CODE_ANCESTRY)
    node1 = tree.body[1].body[2].body[1].value
    node2 = tree.body[1].body[2].body[2].value
    node3 = tree.body[1].body[2].body[3].value
    node4 = tree.body[1].body[2].body[4].value
    node5 = tree.body[1].body[2].body[5].value
    name1 = decode(tree, node1)
    name2 = decode(tree, node2)
    name3 = decode(tree, node3)
    name4 = decode(tree, node4)
    name5 = decode(tree, node5)
    assert name1 == "typing.List"
    assert name2 == "typing.Dict"
    assert name3 == "Union"
    assert name4 == "typing.Tuple"
    assert name5 == "typing.Set"


CODE_ASSIGNMENT = """
import os.path

X = os.path

X
X.join
"""


def test_assignment():
    tree = ast.parse(CODE_ASSIGNMENT)
    node1 = tree.body[2].value
    node2 = tree.body[3].value
    name1 = decode(tree, node1)
    name2 = decode(tree, node2)
    assert name1 == "os.path"
    assert name2 == "os.path.join"


CODE_RELATIVE_IMPORTS = """
from .foo import X
from ..bar import Y
X
Y
"""


def test_relative_imports():
    tree = ast.parse(CODE_RELATIVE_IMPORTS)
    node1 = tree.body[2].value
    node2 = tree.body[3].value
    name1 = decode(tree, node1)
    name2 = decode(tree, node2)
    assert name1 == ".foo.X"
    assert name2 == "..bar.Y"
