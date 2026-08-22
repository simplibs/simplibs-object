"""
Tests for `_core/metadata/init_processors/methods/verifiers/classmethod/verify_classmethod.py`.
"""
import pytest
from simplibs.object import SimpleConstant, SimpleObject
from simplibs.object.exceptions import SimpleDefinitionError


def _int_const(name, default=0):
    return type(name, (SimpleConstant,), {"_type": int, "_default": default})


class TestVerifyClassmethodMissing:

    def test_missing_logic_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)


class TestVerifyClassmethodNotCallable:

    def test_logic_as_plain_attribute_raises(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)
                _logic = "not-a-method"


class TestVerifyClassmethodNotClassmethod:

    def test_logic_as_instance_method_raises_definition_error(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)

                def _logic(self, first):
                    return first

    def test_logic_as_staticmethod_raises_definition_error(self):
        First = _int_const("First")

        with pytest.raises(SimpleDefinitionError):
            class Single(SimpleObject):
                _type = int
                _inners = (First,)

                @staticmethod
                def _logic(cls, first):
                    return first


class TestVerifyClassmethodOptionalDecompose:

    def test_missing_decompose_does_not_raise_and_marks_not_decomposeable(self):
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        assert Single.meta.is_decomposeable is False

    def test_present_decompose_marks_decomposeable(self):
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

            @classmethod
            def _decompose(cls, value):
                return (value,)

        assert Single.meta.is_decomposeable is True

    def test_deep_subclass_without_decompose_remains_not_decomposeable(self):
        First = _int_const("First")

        class Parent(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        class Child(Parent):
            pass

        assert Child.meta.is_decomposeable is False

    def test_deep_subclass_inherits_custom_decompose_from_parent(self):
        First = _int_const("First")

        class Parent(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

            @classmethod
            def _decompose(cls, value):
                return (value,)

        class Child(Parent):
            pass

        assert Child.meta.is_decomposeable is True


class TestVerifyClassmethodDeepSubclassIsolation:

    def test_deep_subclass_reusing_parent_logic_without_structural_override_is_fine(self):
        First = _int_const("First")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        class SingleVariant(Single):
            pass

        assert SingleVariant.calculate_value(9) == 9

    def test_deep_subclass_overriding_type_triggers_clone_and_is_isolated(self):
        First = _int_const("First")
        Second = _int_const("Second")

        class Single(SimpleObject):
            _type = int
            _inners = (First,)

            @classmethod
            def _logic(cls, first):
                return first

        class Pair(Single):
            _type = int
            _inners = (First, Second)

            @classmethod
            def _logic(cls, first, second):
                return first + second

        assert Single.calculate_value(4) == 4
        assert Pair.calculate_value(2, 3) == 5