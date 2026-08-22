"""
Tests for `tools/randomize/random_data_filler.py`.

Mocks `randomize_value` within the tested module to isolate and test
the traversal and decision logic of `random_data_filler` independently
(skip_immutable, is_constant vs. is_decomposeable branching, recursion into inners).
"""
import importlib
import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.object.tools.randomize.random_data_filler import random_data_filler

random_data_filler_module = importlib.import_module(
    "simplibs.object.tools.randomize.random_data_filler"
)


@pytest.fixture
def fake_randomize_value(monkeypatch):
    """Replaces real randomization with deterministic call recording."""
    calls = []

    def _fake(instance, *, retries, registry, skip_unregistered, validate):
        calls.append(instance)
        return instance

    monkeypatch.setattr(random_data_filler_module, "randomize_value", _fake)
    return calls


class TestRandomDataFillerAtomicConstant:

    def test_calls_randomize_value_once_for_plain_constant(self, IntConst, fake_randomize_value):
        instance = IntConst()
        result = random_data_filler(instance)

        assert result is instance
        assert fake_randomize_value == [instance]


class TestRandomDataFillerImmutableBypass:

    def test_locked_or_immutable_instance_is_skipped(self, IntConst, fake_randomize_value):
        instance = IntConst(mutable=False)
        result = random_data_filler(instance, skip_immutable=True)

        assert result is instance
        assert fake_randomize_value == []

    def test_skip_immutable_false_still_processes_immutable_instance(
        self, IntConst, fake_randomize_value
    ):
        instance = IntConst(mutable=False)
        random_data_filler(instance, skip_immutable=False)
        assert fake_randomize_value == [instance]


class TestRandomDataFillerCompositeRecursion:

    def test_recurses_into_inner_instances(self, NonDecomposablePairObject, fake_randomize_value):
        instance = NonDecomposablePairObject(mixins=())
        random_data_filler(instance)

        # NonDecomposablePairObject is not decomposable, so the root is not
        # randomized directly (is_constant False, is_decomposeable False),
        # but both atomic constant inners are randomized.
        assert instance._first in fake_randomize_value
        assert instance._second in fake_randomize_value
        assert instance not in fake_randomize_value

    def test_decomposeable_composite_is_randomized_directly_too(
        self, PairObject, fake_randomize_value
    ):
        instance = PairObject(mixins=())
        random_data_filler(instance)

        assert instance in fake_randomize_value
        assert instance._first in fake_randomize_value
        assert instance._second in fake_randomize_value


class TestRandomDataFillerParameterValidation:

    def test_non_simple_constant_instance_raises(self):
        with pytest.raises(SimpleRuntimeError):
            random_data_filler("not-an-instance")

    def test_zero_retries_raises(self, IntConst):
        instance = IntConst()
        with pytest.raises(SimpleRuntimeError):
            random_data_filler(instance, retries=0)


class TestRandomDataFillerReturnsRoot:

    def test_returns_the_same_root_instance_object(self, IntConst, fake_randomize_value):
        instance = IntConst()
        result = random_data_filler(instance)
        assert result is instance