__version__ = '0.13.22.dev2'

import os

from .document import Document
from .array import DocumentArray
from .dataclasses import dataclass, field

if 'DA_RICH_HANDLER' in os.environ:
    from rich.traceback import install

    install()
