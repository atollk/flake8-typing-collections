"""
Decodes/dereferences import aliases.

When working with an ast, for example to create a static type checker, you
might run into the situation in which you would like to know what object
an ast.Name node refers to. For example, `ElementTree` might refer to
the module `xml.etree.ElementTree` or the class of the same name within
that module, depending on the surrounding imports.
This module tries to decode these situations and return the full name
of the object in question.
"""

import ast
import collections
import itertools
from typing import Dict, Iterable, List, Sequence, Union


def decode(
    whole_tree: ast.AST, node_in_question: Union[ast.Name, ast.Attribute]
) -> str:
    """
    Decodes the object in question.

    The process takes into account import statements as well as up to a single
    assign statement.

    .. code-block:: python
        from os import path as p
        pth = p
        # Decoding "pth" will find "os.path".

    The function is not attempting to be "perfect". For example, if the
    identifier in question is defined multiple times, the decoder will
    not try to work out which of those definitions is the most recent
    to the node, even if it would be possible.

    One exception is a heuristic applied on "try-catch" constructs: for these,
    the checker always assume for the "try" to succeed and skips "catch"
    segments.

    :param whole_tree: The entire AST in which the node is contained in.
    :param node_in_question: The node of type :class:`ast.Name` or :class:`ast.Attribute`, that is to be decoded.
    :return: The complete name of the given identifier as a string. If no better match can be found, the name stored within the :class:`ast.Name` node is returned.
    :raises: The node in question and all its descendents must be of type :class:`ast.Name` or :class:`ast.Attribute`, otherwise a :class:`TypeError` will be raised.
    :raises: If the node describes an empty identifier, a :class:`ValueError` is raised.
    """
    node_id = _build_node_identifier(node_in_question).split(".")
    if not node_id:
        raise ValueError("Cannot decode an empty identifier.")
    ancestors = _ast_ancestors(whole_tree, node_in_question)
    statements_to_analyze = list(_relevant_statements(ancestors))
    alias_dict = _analyze(statements_to_analyze)

    for i in range(len(node_id)):
        lhs = ".".join(node_id[: len(node_id) - i])
        rhs = ".".join(node_id[len(node_id) - i :])
        if lhs in alias_dict:
            lhs = alias_dict[lhs]
            break
    if lhs and rhs:
        return lhs + "." + rhs
    else:
        return lhs + rhs


def _build_node_identifier(node: Union[ast.Name, ast.Attribute]) -> str:
    """
    Converts a named node to a string.

    For nodes of type :class:`ast.Name`, this is simple. For nodes of type
    :class:`ast.Attribute`, the different attribute parts have to be
    concatenated.

    :param node: The node to be converted.
    :return: The name that is represented by the node, as a string.
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return _build_node_identifier(node.value) + "." + node.attr
    else:
        raise TypeError("Can only decode nodes of type ast.Name and ast.Attribute.")


def _ast_ancestors(tree: ast.AST, node: ast.AST) -> List[ast.AST]:
    """
    Finds a list of ancestors from a given node to its root.

    :param tree: The root of the given ast.
    :param node: A node within the given ast.
    :return: A list of nodes such that the first value is ``node``, the last value is ``tree``, and each list element is a child node of its successive element.
    :raises: ``tree`` must be an ancestor of ``node``, i.e. ``node`` must be containedi in ``ast.walk(tree)``. Otherwise, a :class:`KeyError` is raised.
    """
    parent_map = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    ancestors = [node]
    while node != tree:
        node = parent_map[node]
        ancestors.append(node)
    return ancestors


def _relevant_statements(ancestors: List[ast.AST]) -> Iterable[ast.AST]:
    """
    Given a list of ancestors, finds the statements to analyze.

    Given a list of ancestors, as described by :func:`_ast_ancestors`, finds
    all statements in the tree that are considered "worthy to be analyzed".
    In general, these are all child nodes of any ancestor that represent
    import statements or assign statements.

    :param ancestors: The list of ancestors, as described by :func:`_ast_ancestors`.
    :return: An iteration over the relevant nodes.
    """
    acceptable_types = [ast.Import, ast.ImportFrom, ast.Assign]
    for ancestor in ancestors:
        for child in ast.iter_child_nodes(ancestor):
            if any(isinstance(child, t) for t in acceptable_types):
                yield child
            elif isinstance(child, ast.Try):
                for grandchild in itertools.chain(
                    child.body, child.finalbody, child.orelse
                ):
                    if any(isinstance(grandchild, t) for t in acceptable_types):
                        yield grandchild


def _analyze(statements: Sequence[ast.AST]) -> Dict[str, str]:
    """
    Analyzes the given list of statements for all possible identifiers.

    The returned dict will map each potential alias to its full name.
    Full names are not contained, so if an identifier is not present as a key,
    it should be considered to be the full name already.

    :param statements: The sequence of statements, as returned by :func:`_relevant_statements`.
    :return: A dict mapping aliases to full names.
    """
    potential_aliases = collections.defaultdict(list)
    assignments = []
    for statement in statements:
        if isinstance(statement, ast.Assign):
            assignments.append(statement)
        elif isinstance(statement, ast.Import):
            for alias in statement.names:
                if alias.asname is not None:
                    potential_aliases[alias.asname].append(alias.name)
        elif isinstance(statement, ast.ImportFrom):
            for alias in statement.names:
                fullname = ("." * statement.level) + statement.module + "." + alias.name
                if alias.asname is None:
                    potential_aliases[alias.name].append(fullname)
                else:
                    potential_aliases[alias.asname].append(fullname)
        else:
            raise KeyError(f"{statement} cannot be analyzed.")

    for statement in assignments:
        if isinstance(statement.value, ast.Name) or isinstance(
            statement.value, ast.Attribute
        ):
            if len(statement.targets) == 1:
                try:
                    value_identifier = _build_node_identifier(statement.value)
                    target = _build_node_identifier(statement.targets[0])
                except TypeError:
                    continue
                potential_aliases[target] += potential_aliases.get(
                    value_identifier, [value_identifier]
                )

    return {
        alias: fullnames[0]
        for alias, fullnames in potential_aliases.items()
        if len(fullnames) == 1
    }
