__all__ = ["in_notebook", "to_notebook"]


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
DEFAULT_LEAVE = False
DEFAULT_PREFIX = "Download: "
DEFAULT_SUFFIX = ""


def in_notebook(
    file: TPathLike,
    /,
    *,
    leave: bool = DEFAULT_LEAVE,
    prefix: str = DEFAULT_PREFIX,
    suffix: str = DEFAULT_SUFFIX,
) -> TPathLike:
    """Save a file directly into a Jupyter notebook.

    Unlike ``to_notebook``, where file saving is performed immediately,
    it will be deferred until after cell running is completed.
    So this function is intended to be called together with file saving
    by another library, in a manner of wrapping the path of the file.
    See also the examples below.

    Args:
        file: Path of the file to be saved.
        leave: Whether to leave the original file.
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
                to_notebook(file, leave=leave, prefix=prefix, suffix=suffix)
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
    """Convert a file to a download link with its data embedded.

    Args:
        file: Path of the file to be embedded.
        prefix: Prefix of the download link.
        suffix: Suffix of the download link.

    Returns:
        Download link with the file data embedded.

    """
    with open(file := Path(file), "+rb") as f:
        data = b64encode(f.read()).decode()

    href = f"data:{guess_type(file)[0]};base64,{data}"
    link = f"<a download='{file.name}' href='{href}' target='_blank'>{file}</a>"
    return HTML(f"<p>{prefix}{link}{suffix}</p>")


def to_notebook(
    file: PathLike,
    /,
    *,
    leave: bool = DEFAULT_LEAVE,
    prefix: str = DEFAULT_PREFIX,
    suffix: str = DEFAULT_SUFFIX,
) -> None:
    """Save a file directly into a Jupyter notebook.

    A download link will be displayed after the file is saved.
    By default, the original file will be then deleted.
    Specify ``leave=True`` in order to avoid deletion.

    Args:
        file: Path of the file to be saved.
        leave: Whether to leave the original file.
        prefix: Prefix of the download link.
        suffix: Suffix of the download link.

    Examples::

        import matplotlib.pyplot as plt

        plt.plot([1, 2, 3])
        plt.savefig("plot.pdf")
        to_notebook("plot.pdf")

    """
    display(to_html(file, prefix=prefix, suffix=suffix))

    if not leave:
        Path(file).unlink(missing_ok=True)
