"""
Turn a KDL document into a dict, following a set of very simple rules.
"""

from typing import Any, Callable
from typing import Collection

import kdl
from kdl.parsing import ParseConfig


class KDLTransformException(Exception):
    pass


def _nodes_to_dict(node_list: Collection[kdl.Node], root_name: str) -> dict[str, Any]:
    ret = {}

    for node in node_list:
        if node.tag is not None:
            raise KDLTransformException("cuddly_dicts can't handle tags")

        match node:
            # Simple property
            case kdl.Node(name=name, args=[value], nodes=[]) if len(node.props) == 0:
                if thing := ret.get(name):
                    if isinstance(thing, list):
                        thing.append(value)
                    else:
                        ret[name] = [thing, value]
                    
                    continue

                ret[name] = value

            # Node with no args and some properties
            case kdl.Node(name=name, args=[], props=props, nodes=nodes):
                value = {**_nodes_to_dict(nodes, f"{root_name}.{name}"), **props}
                
                if thing := ret.get(name):
                    if isinstance(thing, list):
                        thing.append(value)
                    else:
                        ret[name] = [thing, value]

                ret[name] = value

            # Node with args and properties
            case kdl.Node(name=name, args=[arg], props=props, nodes=nodes):
                node_dict = ret.get(name, {})
                if not isinstance(node_dict, dict):
                    raise KDLTransformException(
                        f"{name} already exists on {root_name} and isn't a dictionary"
                    )

                node_dict[arg] = {
                    **_nodes_to_dict(nodes, f"{root_name}.{name}.{arg}"),
                    **props,
                }

                ret[name] = node_dict

            case _:
                raise KDLTransformException(f"node {node} didn't match any rules")

    return ret


def kdl_document_to_dict(document: kdl.Document) -> dict[str, Any]:
    return _nodes_to_dict(document.nodes, "", value_converters)


def kdl_source_to_dict(source: str, value_converters: dict[str, Callable[[Any], Any]] = {}) -> dict[str, Any]:
    document = kdl.parse(source, ParseConfig(valueConverters=value_converters))
    return kdl_document_to_dict(document)
