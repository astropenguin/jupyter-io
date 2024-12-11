# standard library
from pathlib import Path
from tempfile import NamedTemporaryFile


# dependencies
from jupyter_io.io import to_html


def test_to_html() -> None:
    with NamedTemporaryFile("w", suffix=".txt") as f:
        f.write("1, 2, 3\n")
        f.seek(0)

        file = Path(f.name)
        href = "data:text/plain;base64,MSwgMiwgMwo="
        link = f"<a download='{file.name}' href='{href}' target='_blank'>{file}</a>"
        assert to_html(file, prefix="", suffix="").data == f"<p>{link}</p>"
