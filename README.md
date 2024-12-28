# jupyter-io

[![Release](https://img.shields.io/pypi/v/jupyter-io?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/jupyter-io/)
[![Python](https://img.shields.io/pypi/pyversions/jupyter-io?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/jupyter-io/)
[![Downloads](https://img.shields.io/pypi/dm/jupyter-io?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/jupyter-io)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.14379974-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.14379974)
[![Tests](https://img.shields.io/github/actions/workflow/status/astropenguin/jupyter-io/tests.yaml?label=Tests&style=flat-square)](https://github.com/astropenguin/jupyter-io/actions)

Saving and loading files directly into Jupyter notebooks

## Installation

```shell
pip install jupyter-io
```

## File saving

jupyter-io provides the `in_notebook` function to directly save (i.e. embed) files to Jupyter notebooks.
Suppose you create a Matplotlib figure want to save it as a PDF file.
The following code will save the PDF file to your local environment:
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3])
plt.savefig("figure.pdf")
```
This should work in many cases, however, in a virtual environment like [Google Colaboratory](https://colab.research.google.com/), you will not be able to get the file once the Jupyter server is stopped.
By wrapping the file path by `in_notebook`, the PDF file will be directly saved to the Jupyter notebook and you will get a download link instead:
```python
import matplotlib.pyplot as plt
from jupyter_io import in_notebook

plt.plot([1, 2, 3])
plt.savefig(in_notebook("figure.pdf"))
```
The download link works when the Jupyter server is stopped, and even when it does not exist.
This makes Jupyter notebooks more portable, for example, to share the output data other than images together with them.

### More examples

To save a pandas series to a notebook:

```python
import pandas as pd
from jupyter_io import in_notebook

ser = pd.Series([1, 2, 3])
ser.to_csv(in_notebook("series.csv"))
```

To save a general text to a notebook:

```python
from jupyter_io import in_notebook

with open(in_notebook("output.txt"), "w") as f:
    f.write("1, 2, 3\n")
```

## File loading

The file loading feature has not been implemented yet.
