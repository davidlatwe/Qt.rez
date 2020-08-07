## Qt.py in Rez

A [Rez](https://github.com/nerdvegas/rez) package that works as shim around all Qt binding packages.

```python
# in any Qt App's package.py
requires = [
    "Qt.py",  # Hey Rez, resolve a proper binding.
]
```

#### Usage

First, make sure Rez can access at least one of the binding package. [`rez-pipz`](https://github.com/mottosso/rez-pipz) could help.

And then,
```bash
$ git clone https://github.com/davidlatwe/Qt.rez.git
$ cd Qt.rez
$ rez-build --install
```

#### How it works

While building this package, it will try to find if there are any bindings that has installed as Rez package.

If found, binding packages will be used as the variant of this package.

```python
# in Qt.rez's package.py, pseudo code
@early()
def variants():
    bindings = [
        "PyQt5",
        "PySide2",
        "PyQt4",
        "PySide",
    ]
    variants_ = [
        [binding] for binding in bindings if installed(binding)
    ]
    if not variants_:
        raise Exception("No Qt binding package found.")

    return variants_
```
This binding as variant setup will enable Rez to resolve proper binding package for the requests, without explicitly requesting binding packages.
