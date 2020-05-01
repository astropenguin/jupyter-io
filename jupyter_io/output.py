__all__ = ["savefile_in_notebook", "savefig_in_notebook", "savetable_in_notebook"]


# standard library
from io import BytesIO, StringIO
from base64 import b64encode
from mimetypes import guess_type
from pathlib import Path
from typing import IO, Optional, Union


# dependent packages
from IPython.display import HTML
from matplotlib.pyplot import Figure, gcf
from pandas import DataFrame, Series


# type aliases
PathLike = Union[Path, str]


# main functions
def savefile_in_notebook(f: IO, filename: PathLike, encoding: str = "utf-8") -> HTML:
    """Save file object in a notebook as a Base64 file.

    Args:
        f: File object to be saved.
        filename: Name of a saved file.
        encoding: Text encoding. It is only used if ``f`` is a ``StringIO`` object.

    Returns:
        html: HTML object which shows the download link.

    """
    f.seek(0)
    data = f.read()

    try:
        data = data.encode(encoding)
    except AttributeError:
        pass
    finally:
        base64 = b64encode(data).decode()

    filename = Path(filename).name
    href = f"data:{guess_type(filename)[0]};base64,{base64}"

    anchor = f'<a download="{filename}" href="{href}" target="_blank">{filename}</a>'
    return HTML(f"<p>Download: {anchor}</p>")


def savefig_in_notebook(
    fig: Optional[Figure] = None, filename: PathLike = "figure.pdf", **kwargs,
) -> HTML:
    """Save matplotlib figure in a notebook as a file.

    Args:
        fig: Matplotlib ``Figure`` object to be saved.
        filename: Filename with explicit extension (e.g., ``figure.pdf``).
        **kwargs: Arguments to be passed to matplotlib ``savefig()``.

    Returns:
        html: HTML object which shows the download link.

    """
    if fig is None:
        fig = gcf()

    format_ = Path(filename).suffix.lstrip(".")
    kwargs.setdefault("format", format_)

    with BytesIO() as f:
        fig.savefig(f, **kwargs)
        return savefile_in_notebook(f, filename)


def savetable_in_notebook(
    table: Union[DataFrame, Series], filename: PathLike = "table.csv", **kwargs,
):
    """Save pandas DataFrame or Series in a notebook as a file.

    Args:
        table: pandas ``DataFrame`` of ``Series object`` to be saved.
        filename: Filename with explicit extension (e.g., ``table.csv``).
        **kwargs: Arguments to be passed to ``table.to_<extension>()``.

    Returns:
        html: HTML object which shows the download link.

    """
    format_ = Path(filename).suffix.lstrip(".")

    with StringIO() as f:
        getattr(table, f"to_{format_}")(f, **kwargs)
        return savefile_in_notebook(f, filename)
