# just include production. This does not exist in the repo.
# There's a production skeleton file which contains an example if you need one.

try:
    from .production import *
except ImportError:
    print("Please create a production.py in the settings directory")

