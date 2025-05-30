#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from ooce.exceptions import OutOfContextError

def test_general():

    with pytest.raises(OutOfContextError):
        raise OutOfContextError
