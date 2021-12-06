from . import _version
from .interactive import EpicsArchive

__version__ = _version.get_versions()["version"]

__all__ = [
    "EpicsArchive",
]
