__all__ = [
    # submodules
    "save",
    # aliases
    "to_html",
    "in_notebook",
]
__version__ = "1.0.0"


# submodules
from . import save


# aliases
from .save import to_html, in_notebook
