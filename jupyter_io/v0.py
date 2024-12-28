__all__ = ["savefile_in_notebook", "savefig_in_notebook", "savetable_in_notebook"]


# standard library
from pathlib import Path
from typing import Any, BinaryIO, Optional, TextIO, Union, overload
from warnings import catch_warnings, simplefilter, warn


# dependencies
from matplotlib.figure import Figure
from matplotlib.pyplot import gcf
from pandas import DataFrame, Series
from .io import PathLike, in_notebook


@overload
def savefile_in_notebook(
    f: TextIO,
    filename: PathLike,
    encoding: str = "utf-8",
) -> None: ...


@overload
def savefile_in_notebook(
    f: BinaryIO,
    filename: PathLike,
) -> None: ...


def savefile_in_notebook(
    f: Any,
    filename: PathLike,
    encoding: str = "utf-8",
) -> None:
    """Save file object (I/O object) in a notebook as a file.

    Warning:
        This function is deprecated and will be removed in a future release.
        Use ``jupyter_io.in_notebook`` instead like::

            with open(in_notebook(filename), 'w') as g:
                g.write(f.read())

    Args:
        f: File object (I/O object) to be saved.
        filename: Filename of the saved file.
        encoding: Text encoding. It is only used if ``io`` is a text IO.

    """
    with catch_warnings():
        simplefilter("always", DeprecationWarning)
        warn(
            "This function is deprecated and will be removed in a future release. "
            "Use jupyter_io.in_notebook function instead like: "
            "g = open(in_notebook(filename), 'w'); g.write(f.read())",
            DeprecationWarning,
        )

    f.seek(0)

    if hasattr(data := f.read(), "encode"):
        data = data.encode(encoding)

    with open(in_notebook(filename), "w") as g:
        g.write(data)


def savefig_in_notebook(
    fig: Optional[Figure] = None,
    filename: PathLike = "figure.pdf",
    **kwargs: Any,
) -> None:
    """Save matplotlib figure in a notebook as a file.

    Warning:
        This function is deprecated and will be removed in a future release.
        Use ``jupyter_io.in_notebook`` instead like::

            fig.savefig(in_notebook(filename))

    Args:
        fig: Matplotlib ``Figure`` object to be saved.
        filename: Filename with explicit extension (e.g., ``figure.pdf``).
        **kwargs: Arguments to be passed to matplotlib ``savefig()``.

    """
    with catch_warnings():
        simplefilter("always", DeprecationWarning)
        warn(
            "This function is deprecated and will be removed in a future release. "
            "Use jupyter_io.in_notebook function instead like: "
            "fig.savefig(in_notebook(filename))",
            DeprecationWarning,
        )

    if fig is None:
        fig = gcf()

    fig.savefig(in_notebook(filename), **kwargs)


def savetable_in_notebook(
    table: Union[DataFrame, "Series[Any]"],
    filename: PathLike = "table.csv",
    **kwargs: Any,
) -> None:
    """Save pandas DataFrame or Series in a notebook as a file.

    Warning:
        This function is deprecated and will be removed in a future release.
        Use ``jupyter_io.in_notebook`` instead like::

            table.to_csv(in_notebook(filename))

    Args:
        table: pandas ``DataFrame`` of ``Series object`` to be saved.
        filename: Filename with explicit extension (e.g., ``table.csv``).
        **kwargs: Arguments to be passed to ``table.to_<extension>()``.

    """
    with catch_warnings():
        simplefilter("always", DeprecationWarning)
        warn(
            "This function is deprecated and will be removed in a future release. "
            "Use jupyter_io.in_notebook function instead like: "
            "table.to_csv(in_notebook(filename))",
            DeprecationWarning,
        )

    format_ = Path(filename).suffix.lstrip(".")
    getattr(table, f"to_{format_}")(in_notebook(filename), **kwargs)
