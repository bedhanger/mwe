import sys
from contextlib import redirect_stdout as cout

from .asleeps import main

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
