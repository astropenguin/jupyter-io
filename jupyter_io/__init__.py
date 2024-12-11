__all__ = [
    # submodules
    "v0",
    "save",
    # aliases
    "to_html",
    "in_notebook",
    "savefile_in_notebook",
    "savefig_in_notebook",
    "savetable_in_notebook",
]
__version__ = "1.0.0"


# submodules
from . import v0
from . import save


# aliases
from .v0 import (
    savefile_in_notebook,
    savefig_in_notebook,
    savetable_in_notebook,
)
from .save import to_html, in_notebook
