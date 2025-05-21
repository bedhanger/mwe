"""Self-pylint..."""

from pathlib import Path

# pylint: disable=import-self
from support.runpylint import PyLintRunner

# Explain
help(vars(PyLintRunner)['__module__'])

# Create and init runner, enter context, and run
with PyLintRunner(file=Path(__file__).resolve()) as SPL:
    print('So we can now let our pylint runner loose:', SPL)
    SPL()
