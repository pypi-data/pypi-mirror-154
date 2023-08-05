# contextlib-chdir

Backport of [`contextlib.chdir`] stdlib class added in Python3.11.

## Install

```
pip install contextlib-chdir
```

## Usage

```python
import os
import tempfile
from contextlib_chdir import chdir as chdir_ctx

with chdir_ctx(tempfile.gettempdir()):
    print(os.getcwd())  # /tmp
```

## Note

You'll probably want to migrate to [`contextlib2`] when
[this change is included](https://github.com/jazzband/contextlib2/issues/43).

[`contextlib.chdir`]: https://docs.python.org/3.11/library/contextlib.html#contextlib.chdir
[`contextlib2`]: https://github.com/jazzband/contextlib2
