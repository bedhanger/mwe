#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from requiresthat import requires, RequirementNotFulfilledError

class TestCase_requiresthat_01:

    def test_good(self):

        class Spam:
            def __init__(self):
                self.foo = 66
                self.bar = None

            @requires(that='self.foo == 66')
            @requires(that='self.bar is None')
            def run(self):
                print('Running')

        S = Spam()
        S.run()

    def test_bad(self):

        class Spam:
            def __init__(self):
                self.foo = 66
                self.bar = ... # To be continued, not None

            @requires(that='self.foo == 66')
            @requires(that='self.bar is None')
            def run(self):
                print('Running')

        S = Spam()
        with pytest.raises(RequirementNotFulfilledError):
            S.run()

    @pytest.mark.filterwarnings("ignore::SyntaxWarning")
    def test_ugly(self):

        class Spam:
            def __init__(self):
                pass

            @requires(that=b"'24' is not 'the answer'")
            def run(self):
                print('Running')

        S = Spam()
        S.run()
