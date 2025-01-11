#!/usr/bin/env python
"""
Pylint (yerself)
Use it the way it uses itself
Run it last in your code, as it currently "replaces the interpreter"
"""
class PyLintRunner:
    """
    The class from which a runner for pylint may be instantiated from
    """
    def __init__(self, file):
        self._file = file
        try:
            # A calculated concession...
            # pylint: disable=import-outside-toplevel
            from pylint import run_pylint
        except (ModuleNotFoundError, ImportError):
            from warnings import simplefilter, warn
            simplefilter('default')
            warn('No self-pylinting: requisite infrastructure not found', category=ImportWarning)
        self._run_pylint = run_pylint

    def run(self) -> None:
        """
        Try to lint the file
        """
        self._run_pylint(argv=[self._file])

    def destroy(self) -> None:
        """
        Destroy ourselves
        """
        del self

# It would be hypocritical not to do this here
if __name__ == '__main__':
    # The import below is, of course, not required *here*, but because we would like to show how
    # self-pylinting can be used *elsewhere*, we carry it out after saying it's ok...
    # In the real world, don't disable the rule and simply pay attention to the where the import
    # should go
    # pylint: disable=import-self
    from support.selfpylint.linter import PyLintRunner
    SPL = PyLintRunner(__file__)
    SPL.run()
    SPL.destroy()
