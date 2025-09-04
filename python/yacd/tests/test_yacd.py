#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from inspect import isclass

from yacd import singleton, nullfiy, instancify


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
