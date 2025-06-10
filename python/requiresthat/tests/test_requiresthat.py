#!/usr/bin/env --split-string=python -m pytest --verbose

from requiresthat import requires

class TestCase_requiresthat_01:

    def test_general(self):

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
