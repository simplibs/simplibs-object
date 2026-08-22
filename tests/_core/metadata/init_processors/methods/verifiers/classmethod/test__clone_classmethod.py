"""
Tests for `_core/metadata/init_processors/methods/verifiers/classmethod/_clone_classmethod.py`.

Tests directly on a real `classmethod` object to verify that the clone is functionally
equivalent but completely isolated (mutating defaults/annotations on the clone does not
affect the original).
"""
from simplibs.object._core.metadata.init_processors.methods.verifiers.classmethod._clone_classmethod import (
    _clone_classmethod,
)


class Original:
    @classmethod
    def compute(cls, a, b=2):
        """Original docstring."""
        return a + b


class TestCloneClassmethodFunctionalEquivalence:

    def test_clone_produces_same_result(self):
        clone = _clone_classmethod(Original.__dict__["compute"])
        bound_clone = clone.__get__(None, Original)
        assert bound_clone(3) == 5
        assert bound_clone(3, 10) == 13

    def test_clone_is_classmethod_instance(self):
        clone = _clone_classmethod(Original.__dict__["compute"])
        assert isinstance(clone, classmethod)

    def test_clone_preserves_function_name(self):
        clone = _clone_classmethod(Original.__dict__["compute"])
        assert clone.__func__.__name__ == "compute"


class TestCloneClassmethodIsolation:

    def test_mutating_clone_defaults_does_not_affect_original(self):
        original_cm = Original.__dict__["compute"]
        clone = _clone_classmethod(original_cm)

        clone.__func__.__defaults__ = (99,)

        assert original_cm.__func__.__defaults__ == (2,)
        assert clone.__func__.__defaults__ == (99,)

    def test_mutating_clone_annotations_does_not_affect_original(self):
        original_cm = Original.__dict__["compute"]
        clone = _clone_classmethod(original_cm)

        clone.__func__.__annotations__["a"] = int

        assert "a" not in original_cm.__func__.__annotations__

    def test_clone_copies_custom_function_dict_attributes(self):
        def compute(cls, a):
            return a

        compute.custom_flag = True
        cm = classmethod(compute)

        clone = _clone_classmethod(cm)
        assert clone.__func__.custom_flag is True

        # Ensure dictionary is an isolated copy
        clone.__func__.custom_flag = False
        assert compute.custom_flag is True