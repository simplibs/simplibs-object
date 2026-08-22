"""
Unit tests for `settings/logging.py`.
"""
import logging
from unittest.mock import MagicMock
import pytest

from simplibs.object.settings import logging as simple_logging
from simplibs.object.settings.logging import log_value_event


class DummySimpleClass:
    __name__ = "DummySimpleClass"


@pytest.fixture(autouse=True)
def clean_logging_state():
    """Ensure global callback and logger state are reset after each test."""
    original_callback = simple_logging.on_value_change
    simple_logging.on_value_change = None
    yield
    simple_logging.on_value_change = original_callback


class TestLoggingDefaults:

    def test_default_state(self):
        """Verify default module settings."""
        assert simple_logging.on_value_change is None
        assert simple_logging._logger.name == "simple"


class TestLogValueEventStdlibLogging:

    def test_logs_debug_message_when_debug_enabled(self, caplog):
        """Verify that a message is logged when log level is set to DEBUG."""
        with caplog.at_level(logging.DEBUG, logger="simple"):
            log_value_event(DummySimpleClass, 42, "assign")

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelname == "DEBUG"
        assert record.name == "simple"
        assert record.message == "[assign] DummySimpleClass = 42"

    def test_does_not_log_debug_message_when_level_is_higher(self, caplog):
        """Verify that no message is logged when log level is higher than DEBUG."""
        with caplog.at_level(logging.INFO, logger="simple"):
            log_value_event(DummySimpleClass, 42, "assign")

        assert len(caplog.records) == 0


class TestLogValueEventCallback:

    def test_triggers_registered_callback(self):
        """Verify that a registered callback is correctly triggered with proper arguments."""
        mock_callback = MagicMock()
        simple_logging.on_value_change = mock_callback

        log_value_event(DummySimpleClass, "test_value", "validate")

        mock_callback.assert_called_once_with(DummySimpleClass, "test_value", "validate")

    def test_works_without_callback_without_raising_error(self):
        """Verify that calling without a registered callback runs silently without exceptions."""
        simple_logging.on_value_change = None
        log_value_event(DummySimpleClass, 100, "step")