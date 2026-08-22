"""
Tests for `tools/randomize/randomize_value.py`.

Uses monkeypatching on `randomize`/`RandomizeError` within the tested module
to ensure deterministic testing independently of external packages.
"""
import importlib
import pytest
from simplibs.object.exceptions import SimpleRuntimeError
from simplibs.object.tools.randomize.randomize_value import randomize_value

randomize_value_module = importlib.import_module(
    "simplibs.object.tools.randomize.randomize_value"
)


class _FakeRandomizeError(Exception):
    """Lightweight replacement for simplibs.randomize.RandomizeError for isolated tests."""


@pytest.fixture
def patched_randomize(monkeypatch):
    """Allows tests to configure a deterministic sequence of pseudo-random values."""

    def _apply(values):
        it = iter(values)

        def fake_randomize(value_type):
            try:
                return next(it)
            except StopIteration:
                raise _FakeRandomizeError("exhausted fake values")

        monkeypatch.setattr(randomize_value_module, "randomize", fake_randomize)
        monkeypatch.setattr(randomize_value_module, "RandomizeError", _FakeRandomizeError)

    return _apply


class TestRandomizeValueHappyPath:

    def test_assigns_first_successful_candidate(self, IntConst, patched_randomize):
        instance = IntConst()
        patched_randomize([999])

        result = randomize_value(instance, retries=3, registry=None)

        assert result is instance
        assert instance.value == 999

    def test_skips_candidate_equal_to_current_value(self, IntConst, patched_randomize):
        instance = IntConst()
        current = instance.value
        patched_randomize([current, current, 42])

        randomize_value(instance, retries=5, registry=None)
        assert instance.value == 42

    def test_retries_on_setter_validation_failure(self, PositiveIntConst, patched_randomize):
        instance = PositiveIntConst()
        # First candidate fails custom _validate (negative integer), second succeeds.
        patched_randomize([-5, 5])

        randomize_value(instance, retries=5, registry=None)
        assert instance.value == 5


class TestRandomizeValueExhaustion:

    def test_raises_when_retries_exhausted_without_success(
        self, PositiveIntConst, patched_randomize
    ):
        instance = PositiveIntConst()
        # All candidates are invalid (negative).
        patched_randomize([-1, -2, -3])

        with pytest.raises(SimpleRuntimeError):
            randomize_value(instance, retries=3, registry=None)


class TestRandomizeValueUnregisteredType:

    def test_unregistered_type_reraises_by_default(self, IntConst, monkeypatch):
        def raising_randomize(value_type):
            raise _FakeRandomizeError("unregistered type")

        monkeypatch.setattr(randomize_value_module, "randomize", raising_randomize)
        monkeypatch.setattr(randomize_value_module, "RandomizeError", _FakeRandomizeError)

        instance = IntConst()
        with pytest.raises(_FakeRandomizeError):
            randomize_value(instance, retries=3, registry=None, skip_unregistered=False)

    def test_unregistered_type_skipped_when_flag_set(self, IntConst, monkeypatch):
        def raising_randomize(value_type):
            raise _FakeRandomizeError("unregistered type")

        monkeypatch.setattr(randomize_value_module, "randomize", raising_randomize)
        monkeypatch.setattr(randomize_value_module, "RandomizeError", _FakeRandomizeError)

        instance = IntConst()
        original_value = instance.value
        result = randomize_value(instance, retries=3, registry=None, skip_unregistered=True)

        assert result is instance
        assert instance.value == original_value


class TestRandomizeValueParameterValidation:

    def test_non_simple_constant_instance_raises(self, patched_randomize):
        patched_randomize([1])
        with pytest.raises(SimpleRuntimeError):
            randomize_value("not-an-instance", retries=3, registry=None)

    def test_zero_retries_raises(self, IntConst, patched_randomize):
        instance = IntConst()
        patched_randomize([1])
        with pytest.raises(SimpleRuntimeError):
            randomize_value(instance, retries=0, registry=None)

    def test_negative_retries_raises(self, IntConst, patched_randomize):
        instance = IntConst()
        patched_randomize([1])
        with pytest.raises(SimpleRuntimeError):
            randomize_value(instance, retries=-1, registry=None)

    def test_validate_false_skips_parameter_checks(self, IntConst, patched_randomize):
        """With `validate=False`, internal parameter validation is bypassed.
        An invalid `retries` type reaches the loop and fails with TypeError rather than SimpleRuntimeError.
        """
        instance = IntConst()
        patched_randomize([1])
        with pytest.raises(TypeError):
            randomize_value(instance, retries="not-an-int", registry=None, validate=False)