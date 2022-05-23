import os.path
# Extract central version information
with open(os.path.join(os.path.dirname(__file__), "VERSION")) as version_file:
    version = version_file.read().strip()

__version__ = version
__licence__ = 'MIT'
