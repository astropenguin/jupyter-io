# dependent packages
import pandas as pd
from jupyter_io import savecsv_in_notebook


# constants
expected_csv = (
    '<a download="test.csv" '
    'href="data:text/csv;base64,LDAKMCwwCjEsMQoyLDIKMywzCjQsNAo1LDUKNiw2CjcsNwo4LDgKOSw5Cg==" '
    'target="_blank">Download test.csv</a>'
)


# test functions
def test_savecsv():
    html = savecsv_in_notebook(pd.DataFrame(range(10)), "test.csv")
    assert html.data == expected_csv
