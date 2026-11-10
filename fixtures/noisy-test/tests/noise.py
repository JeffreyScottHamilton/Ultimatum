"""Shared helper: tests announce themselves and trigger legacy warnings."""
import warnings

from pipeline.logutil import legacy


def chatter(test, lines=9):
    print(f"--- begin {test.id()} ---")
    for i in range(lines):
        print(f"  [setup {i + 1}/{lines}] preparing fixture data for {test._testMethodName}")
    warnings.simplefilter("always", DeprecationWarning)
    legacy("setup_helper")
    print(f"--- end setup {test._testMethodName} ---")
