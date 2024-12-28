__all__ = [
    # submodules
    "io",
    "v0",
    # aliases
    "in_notebook",
    "to_notebook",
    "savefile_in_notebook",
    "savefig_in_notebook",
    "savetable_in_notebook",
]
__version__ = "2.0.1"


# submodules
from . import io
from . import v0


# aliases
from .io import in_notebook, to_notebook
from .v0 import savefile_in_notebook, savefig_in_notebook, savetable_in_notebook
