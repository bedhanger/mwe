#!/usr/bin/env python
"""
Pylint (yerself)
"Use it the way it uses itself"

In the absence of (or complementing) unit tests, this can be used to lint any Python file, including
itself as is shown below (it would be hypocritical not to do this).

There are a few well-calculated exceptions to Pylint rules that have been sprinkled in for the
purpose of being able to recover gracefully to the absence of Pylint from the system this runs on,
or else for being able to actually show how to use the module.

So while the code is not fully Pylint-clean, there are good reasons for this.

When *run*, as per

    $   python -msupport.runpylint.pylintrunner

this module *self-pylints (SPLs) itself* like so (look at the source code for the fine details)

    >>> from support.runpylint.pylintrunner import PyLintRunner
    >>> with PyLintRunner(file=__file__) as SPL:
    >>>     SPL()

This handful of statements is what could be placed into "any Python script" and we'd have a recipe
for what might be called Pylint-driven development...
"""

from pathlib import Path
from support.runmwe.mwerunner import MweRunner
from support.pathorstr import PathOrStr

class PyLintRunner(MweRunner):
    """
    A runner for pylint may be instantiated from this to inspect a file
    """

    # Hm...
    # pylint: disable=too-few-public-methods

    def __init__(self, file: PathOrStr):
        """
        Init a newly made Pylint runner
        """
        super().__init__()
        self._file = file
        print('File points to', self._file)
        try:
            # A calculated concession...
            # pylint: disable=import-outside-toplevel
            from pylint.lint import Run as PylintRun
        except (ModuleNotFoundError, ImportError):
            from warnings import simplefilter, warn
            simplefilter('default')
            warn('No self-pylinting: requisite infrastructure not found', category=ImportWarning)
        self._pylintrun = PylintRun
        print('Will invoke function of instance of', self._pylintrun, 'to do the job')

    def __enter__(self):
        super().__enter__()
        assert Path(self._file).exists, 'File not found'
        print('File exists')
        return self

    def __call__(self):
        """
        Try to lint the file
        """
        super().__call__()
        # We need to convert the file into a string because of the way pylint pre-processes options
        # (needs startswith)
        self._pylintrun(args=[str(self._file), '--verbose', '--recursive=y'], exit=False)

if __name__ == '__main__':

    # Self-pylint...

    # pylint: disable=import-self
    from support.runpylint.pylintrunner import PyLintRunner

    # Explain
    help(vars(PyLintRunner)['__module__'])

    # Create and init runner, enter context, and run
    with PyLintRunner(file=Path(__file__).resolve()) as SPL:
        print('So we can now let our pylint runner loose:', SPL)
        SPL()
