#!/usr/bin/env python
"""
Pylint (yerself)
Use it the way it uses itself

In the absence of (or complementing) unit tests, this can be used to lint any Python file, including
itself as is shown below (it would be hypocritical not to do this).

There are a few well-calculated exceptions to Pylint rules that have been sprinkled in for the
purpose of being able to recover gracefully to the absence of Pylint from the system this runs on,
or else for being able to actually show how to use the module.

So while the code is not fully Pylint-clean, there are good reasons for this.
"""
class PyLintRunner:
    """
    The class a runner for pylint may be instantiated from
    """
    def __new__(cls, file):
        _instance = super().__new__(cls)
        print('Creating', _instance, 'to inspect', file)
        return _instance

    def __init__(self, file):
        print('Initialising', self)
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
        print('Will invoke', self._pylintrun,'to do the job')

    def run(self) -> None:
        """
        Try to lint the file
        """
        self._pylintrun(args=[self._file, '--verbose', '--recursive=y'], exit=False)

    def __call__(self):
        """
        Make an instance callable
        """
        self.run()

    def destroy(self) -> None:
        """
        Destroy ourselves
        """
        print('Destructing', self)
        del self

    def __del__(self):
        """
        Finaliser
        """
        self.destroy()

if __name__ == '__main__':

    # pylint: disable=import-self
    from support.selfpylint.linter import PyLintRunner

    help(PyLintRunner)

    SPL = PyLintRunner(file=__file__)

    # This is equivalent to calling SPL.run()
    SPL()

    # Cleanup
    del SPL
