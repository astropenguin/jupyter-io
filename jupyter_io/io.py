__all__ = ["in_notebook", "to_notebook"]


# standard library
from base64 import b64encode
from mimetypes import guess_type
from pathlib import Path
from tempfile import TemporaryDirectory
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

    Unlike ``to_notebook``, where file saving is performed immediately,
    it will be deferred until after cell running is completed.
    So this function is intended to be called together with file saving
    by another library, in a manner of wrapping the path of the file.
    See also the examples below.

    Args:
        file: Path of the file to be saved.
        prefix: Prefix of the download link.
        suffix: Suffix of the download link.

    Returns:
        The same object as ``file``.

    Examples:
        To save a Matplotlib figure into a notebook::

            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3])
            plt.savefig(in_notebook("plot.pdf"))

        To save a pandas series into a notebook::

            import pandas as pd

            ser = pd.Series([1, 2, 3])
            ser.to_csv(in_notebook("series.csv"))

        To save a general text into a notebook::

            with open(in_notebook("output.txt"), "w") as f:
                f.write("1, 2, 3\\n")

    """
    if (ip := get_ipython()) is None:
        raise RuntimeError("Current interactive shell does not exist.")

    tempdir = TemporaryDirectory()
    tempfile = Path(tempdir.name) / Path(file).name

    def callback(result: ExecutionResult, /) -> None:
        try:
            to_notebook(tempfile, prefix=prefix, suffix=suffix)
        finally:
            ip.events.unregister("post_run_cell", callback)
            tempdir.cleanup()

    ip.events.register("post_run_cell", callback)
    return type(file)(tempfile)


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

    download = file.name
    href = f"data:{guess_type(file)[0]};base64,{data}"
    return HTML(f"<p>{prefix}<a {download=} {href=}>{download}</a>{suffix}</p>")


def to_notebook(
    file: PathLike,
    /,
    *,
    prefix: str = DEFAULT_PREFIX,
    suffix: str = DEFAULT_SUFFIX,
) -> None:
    """Save a file directly into a Jupyter notebook.

    A download link will be displayed after the file is saved.
    By default, the original file will be then deleted.
    Specify ``leave=True`` in order to avoid deletion.

    Args:
        file: Path of the file to be saved.
        prefix: Prefix of the download link.
        suffix: Suffix of the download link.

    Examples:
        To save a Matplotlib figure into a notebook::

            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3])
            plt.savefig("plot.pdf")
            to_notebook("plot.pdf")

        To save a pandas series into a notebook::

            import pandas as pd

            ser = pd.Series([1, 2, 3])
            ser.to_csv("series.csv")
            to_notebook("series.csv")

        To save a general text into a notebook::

            with open("output.txt", "w") as f:
                f.write("1, 2, 3\\n")

            to_notebook("output.txt")

    """
    display(to_html(file, prefix=prefix, suffix=suffix))
