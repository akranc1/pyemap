"""
pyemap
Implementation of eMap analysis in the form of a python package.
"""

# Add imports here
from .parse import *
from .process_data import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
