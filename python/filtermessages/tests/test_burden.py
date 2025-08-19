#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest
import re

from filtermessages import DEFAULT_THINGS_CONSIDERED_BORING

class TestCase_burden_01:

    def test_general(self):

        assert DEFAULT_THINGS_CONSIDERED_BORING is not None
        assert isinstance(DEFAULT_THINGS_CONSIDERED_BORING, re.Pattern)
        assert DEFAULT_THINGS_CONSIDERED_BORING.pattern is not None
        assert isinstance(DEFAULT_THINGS_CONSIDERED_BORING.pattern, str)

    def test_trivial_match(self):

        assert DEFAULT_THINGS_CONSIDERED_BORING.search('dvb_frontend_get_frequency_limits')

    def test_protection(self):

        # You cannot create an instance from re.Pattern!
        with pytest.raises(TypeError):
            x = DEFAULT_THINGS_CONSIDERED_BORING()
