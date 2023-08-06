#
# c-apidocs - API Documentation Utilities
#

import re
import sys

import hawkmoth
import hawkmoth.util.compiler
import hawkmoth.util.readthedocs


def hawkmoth_conf():
    try:
        hawkmoth.util.readthedocs.clang_setup()
    except Exception:
        sys.stderr.write('Error: Cannot setup Hawkmoth-clang\n')
        raise


def hawkmoth_converter(data):
    return data


def hawkmoth_include_args():
    return hawkmoth.util.compiler.get_include_args()
