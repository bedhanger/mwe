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

this module *self-pylints (SPLs) itself* like so

    >>> from support.runpylint.pylintrunner import PyLintRunner
    >>> SPL = PyLintRunner(file=__file__)
    >>> SPL()
    >>> del SPL

This handful of statements is what could be placed into "any Python script..."
"""
class PyLintRunner:
    """
    A runner for pylint may be instantiated from this to inspect a file
    """
    def __new__(cls, file):
        _instance = super().__new__(cls)
        print('Creating instance of', _instance, 'to inspect', file)
        return _instance

    def __init__(self, file):
        print('Initialising instance of', self)
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

    def __call__(self):
        """
        Try to lint the file
        """
        self._pylintrun(args=[self._file, '--verbose', '--recursive=y'], exit=False)

    def __del__(self):
        """
        Finalise the runner
        """
        print('Destructing instance of', self)

    def __repr__(self):
        """
        Tell the world who we are, and where
        """
        return str(type(self)) + ' @ ' + hex(id(self))

if __name__ == '__main__':

    # pylint: disable=import-self
    from support.runpylint.pylintrunner import PyLintRunner

    # Explain
    help(vars(PyLintRunner)['__module__'])

    # Create and init runner
    SPL = PyLintRunner(file=__file__)

    # Run
    SPL()

    # Explicit cleanup (here, the scope ending would also do the trick)
    del SPL
