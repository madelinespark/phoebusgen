""" phoebusgen.tools Module

This module contains a Phoebus parser and linter.

Example:
    >>> import phoebusgen.tools
    >>> fp = "./testphoebus.bob"
    >>> my_screen = phoebusgen.tools.parse(fp)
    >>> print(my_screen)
    <?xml version="1.0" ?>
    <display version="2.0.0">
      <name>my screen</name>
    </display>

"""

# Copyright (c) 2022 Lawrence Berkeley National Laboratory,
# Advanced Light Source, Engineering Division

from phoebusgen.tools.parse import *
from phoebusgen.tools.lint import *

__all__ = ['parse', 'lint']
