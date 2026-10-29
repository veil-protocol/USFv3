"""Make `module` and sibling evolution files importable whether this package is
run as a script or imported. Stdlib-only projects don't get packaging for free."""
import pathlib
import sys

_ENGINE = pathlib.Path(__file__).resolve().parent.parent
for _p in (str(_ENGINE), str(_ENGINE / "evolution")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
