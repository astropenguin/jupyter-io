__all__ = ["savefile_in_notebook", "savefig_in_notebook", "savecsv_in_notebook"]

# standard library
from io import BytesIO, StringIO
from base64 import b64encode
from mimetypes import guess_type
from pathlib import Path

# dependent packages
import matplotlib.pyplot as plt
from IPython.display import HTML


def savefile_in_notebook(f, filename, encoding="utf-8"):
    """Embed file object in a notebook with given filename."""
    f.seek(0)
    data = f.read()

    try:
        data = data.encode(encoding)
    except AttributeError:
        pass
    finally:
        base64 = b64encode(data).decode()

    filename = Path(filename).name
    mime = guess_type(filename)[0]
    href = f"data:{mime};base64,{base64}"
    text = f"Download {filename}"
    target = "_blank"

    return HTML(f'<a download="{filename}" href="{href}" target="{target}">{text}</a>')


def savefig_in_notebook(filename, fig=None, **kwargs):
    """Embed matplotlib figure in a notebook with given name."""
    if fig is None:
        fig = plt.gcf()

    format_ = Path(filename).suffix.lstrip(".")
    kwargs.setdefault("format", format_)

    with BytesIO() as f:
        fig.savefig(f, **kwargs)
        return savefile_in_notebook(f, filename)


def savecsv_in_notebook(df, filename, **kwargs):
    """Embed pandas dataframe in a notebook with given name."""
    with StringIO() as f:
        df.to_csv(f, **kwargs)
        return savefile_in_notebook(f, filename)
