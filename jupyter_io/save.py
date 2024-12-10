__all__ = ["in_notebook", "to_html"]


# standard library
from base64 import b64encode
from mimetypes import guess_type
from pathlib import Path
from typing import TypeVar, Union


# dependencies
from IPython.core.getipython import get_ipython
from IPython.core.interactiveshell import ExecutionResult
from IPython.display import HTML, display


# type hints
PathLike = Union[Path, str]
TPathLike = TypeVar("TPathLike", bound=PathLike)


# constants
DEFAULT_PREFIX = "Download: "
DEFAULT_SUFFIX = ""


def in_notebook(
    file: TPathLike,
    /,
    *,
    prefix: str = DEFAULT_PREFIX,
    suffix: str = DEFAULT_SUFFIX,
) -> TPathLike:
    """Save a file directly into a Jupyter notebook.

    The file saving is deferred until after the cell execution is completed,
    and a download link for the file will be then displayed.
    This allows this function to be applied to even files that do not exist.
    See also the examples below.

    Args:
        file: Path of the file to be saved.
        prefix: Prefix of the download link.
        suffix: Suffix of the download link.

    Returns:
        The same object as ``file``.

    Examples::

        import matplotlib.pyplot as plt

        plt.plot([1, 2, 3])
        plt.savefig(in_notebook("plot.pdf"))

    """
    if (ip := get_ipython()) is not None:

        def callback(result: ExecutionResult, /) -> None:
            try:
                display(to_html(file, prefix=prefix, suffix=suffix))
            finally:
                ip.events.unregister("post_run_cell", callback)

        ip.events.register("post_run_cell", callback)

    return file


def to_html(
    file: PathLike,
    /,
    *,
    prefix: str = DEFAULT_PREFIX,
    suffix: str = DEFAULT_SUFFIX,
) -> HTML:
    """Convert a file to an HTML object with its data embedded as a download link.

    Args:
        file: Path of the file to be embedded.
        prefix: Prefix of the download link.
        suffix: Suffix of the download link.

    Returns:
        HTML object with the file data embedded as a download link.

    """
    with open(file, "+rb") as f:
        data = b64encode(f.read()).decode()

    href = f"data:{guess_type(file)[0]};base64,{data}"
    link = f"<a download='{Path(file).name}' href='{href}' target='_blank'>{file}</a>"
    return HTML(f"<p>{prefix}{link}{suffix}</p>")
