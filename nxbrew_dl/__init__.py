from importlib.metadata import version

from .gui import MainWindow

# Get the version
__version__ = version(__name__)

__all__ = [
    "MainWindow",
]
