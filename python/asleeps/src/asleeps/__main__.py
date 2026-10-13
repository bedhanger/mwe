import sys
from contextlib import redirect_stdout as cout
from pathlib import PurePath

try:
    from .asleeps import main
except ImportError:
    py, me = PurePath(sys.executable).name, PurePath(__file__).parent.name
    with cout(sys.stderr):
        print(f'Use "{py} -m {me} ..."')
        print(f'Or try simply "{me}" if it has been installed properly')
    sys.exit(-1)

try:
    sys.exit(main())

except KeyboardInterrupt:
    with cout(sys.stderr):
        print("Interupted by user")
    sys.exit(1)

# ruff: disable[BLE001]
except Exception as exc:
# ruff: enable[BLE001]
    with cout(sys.stderr):
        print(f"Something went awry: {exc=}")
    sys.exit(2)
