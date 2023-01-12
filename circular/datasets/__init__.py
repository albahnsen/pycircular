"""
The :mod:`circular.datasets` module includes utilities to load datasets,
including methods to load and fetch popular reference datasets. It also
features some artificial data generators.
"""

from .base import load_transactions

__all__ = ['load_transactions']