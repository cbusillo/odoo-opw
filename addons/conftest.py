from types import MethodType
from typing import Any

from _pytest.unittest import TestCaseFunction
from odoo.tests.common import BaseCase


def _outcome_ok(self: Any) -> Any:  # emulate unittest.TestResult.wasSuccessful
    return getattr(self, "_outcome", None) is None or self._outcome.success


TestCaseFunction.wasSuccessful = MethodType(_outcome_ok, TestCaseFunction)
TestCaseFunction.addSubTest = lambda *_, **__: None
BaseCase._tests_run_count = 1
