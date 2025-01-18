"""
CLI for cuddly_dicts.
"""

import argparse
import json
from io import StringIO

from cuddly_dicts import kdl_source_to_dict

parser = argparse.ArgumentParser(
    prog="cuddly_dicts", description="Turn a KDL document into JSON"
)
parser.add_argument("filename", type=argparse.FileType("r"), help="File to transform")
parser.add_argument("p", action="store_true", help="Pretty-print the result")


def main(env):
    file: StringIO = env.filename

    ret = kdl_source_to_dict(file.read())
    print(json.dumps(ret, indent=2 if env.p else 0))


if __name__ == "__main__":
    env = parser.parse_args()
    main(env)
