#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from inspect import isclass

from yacd import singleton, nullfiy, instancify, callify


class TestCase_Singleton:

    def test_non_singletons_are_different(self):

        class C: ...

        assert C() is not C()

    def test_singletons_are_equal(self):

        @singleton
        class C: ...

        assert C() is C()


class TestCase_Nullify:

    def test_normal_function(self):

        @nullfiy
        def f():

            raise Exception('why are we here?!?')

        f()

    def test_method(self):

        class C:

            @nullfiy
            def method(self):

                raise Exception('why are we here?!?')

        C().method()

    def test_class__init__(self):

        class C:

            @nullfiy
            def __init__(self):

                raise Exception('why are we here?!?')

            def method(self):

                assert True

        C().method()

    def test_class_instance_creation_fails(self):

        @nullfiy
        class C:

            def __init__(self):

                raise Exception('why are we here?!?')

            def method(self):

                raise Exception('why are we here?!?')

        with pytest.raises(AttributeError):
            C().method()


class TestCase_Instancify:

    def test_class_instance_creation_canonical(self):

        class C: ...

        assert isclass(C)
        assert isinstance(C(), C)
        assert type(C()) is C
        assert type(C) is type

    def test_class_instance_creation_decorated(self):

        @instancify
        class C: ...

        assert not isclass(C)
        assert type(C) is C.__class__
        assert isinstance(C, type(C))
        assert isinstance(C, C.__class__)

    def test_class_instance_creation_decorated_with_init_and_args(self):

        @instancify(spam='ham', eggs='bacon')
        class C:

            def __init__(self, spam, eggs):
                self.spam = spam
                self.eggs = eggs

        assert C.spam == 'ham'
        assert C.eggs == 'bacon'


class TestCase_Callify:

    def test_instance_call_canonical(self):

        class C:

            def __init__(self):
                self.data = 'spam'

            def __call__(self) -> str:
                return self.data

        c = C()

        assert isclass(C)
        assert isinstance(c, C)
        assert c() == 'spam'

    def test_instance_decorated_call(self):

        @instancify # could also use @callify
        class C:

            def __init__(self):
                self.data = 24

            def __call__(self) -> int:
                return self.data

        assert C() == 24

    def test_instance_call_decorated_stacked(self):

        @callify
        @instancify
        class C:

            def __init__(self):
                self.data = 42

            def __call__(self) -> int:
                return self.data

        assert isinstance(C, int)
        assert C == 42

    def test_instance_call_decorated_stacked_with_args(self):

        @callify(addon='World!')
        @instancify(data='Hello')
        class C:

            def __init__(self, data):
                self.data = data

            def __call__(self, addon) -> str:
                return self.data + ', ' + addon

        assert isinstance(C, str)
        assert C == 'Hello, World!'
