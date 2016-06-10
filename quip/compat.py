import sys


if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path
