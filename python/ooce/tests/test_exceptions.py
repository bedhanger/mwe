#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from ooce.exceptions import OutOfContextError

class TestCaseOOCE_01:

    def test_exc_can_be_raised(self):

        with pytest.raises(OutOfContextError):
            raise OutOfContextError
