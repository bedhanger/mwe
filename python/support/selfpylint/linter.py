#!/usr/bin/env python
"""
Pylint yerself
Use it the way it uses itself
"""
def run_selfpylint(file) -> None:
    """
    Try to lint the file this is called in
    """
    try:
        # A calculated concession...
        # pylint: disable=import-outside-toplevel
        from pylint import run_pylint
        run_pylint(argv=[file])
    except (ModuleNotFoundError, ImportError):
        from warnings import simplefilter, warn
        simplefilter('default')
        warn('No self-pylinting: requisite infrastructure not found', category=ImportWarning)

# It would be hypocritical not to do this here
if __name__ == '__main__':
    # The import below is, of course, not required *here*, but because we would like to show how
    # self-pylinting can be used *elsewhere*, we carry it out after saying it's ok...
    # pylint: disable=import-self
    from support.selfpylint.linter import run_selfpylint
    run_selfpylint(__file__)
