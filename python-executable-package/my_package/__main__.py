
import sys
import os

try:
    # This file has been loaded as part of a package (`python -m my_package`)
    from . import main
except (ImportError, SystemError):
    # This file has been loaded independently from its package using the folder
    # syntax (`python my_package/`) or as a zip file (`python my_package.pyz`).
    # In this case, relative imports are not allowed. As a workaround, the
    # directory parent of this one is temporarily added to the path.
    dir_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, dir_path)
    from my_package import main
    sys.path.pop(0)


if __name__ == '__main__':
    sys.exit(main())
