# flake8: noqa


# dependent packages
import pandas as pd
from jupyter_io import savetable_in_notebook


# constants
TABLE_HTML = (
    "<p>Download: "
    '<a download="table.csv" '
    'href="data:text/csv;base64,LDAKMCwwCjEsMQoyLDIKMywzCjQsNAo1LDUKNiw2CjcsNwo4LDgKOSw5Cg==" '
    'target="_blank">table.csv</a>'
    "</p>"
)


# test functions
def test_savetable():
    html = savetable_in_notebook(pd.DataFrame(range(10)), "table.csv")
    assert html.data == TABLE_HTML
