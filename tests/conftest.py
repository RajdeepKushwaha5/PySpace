import os
import pytest


def pytest_collection_modifyitems(config, items):
    """Skip tests marked as 'integration' unless RUN_INTEGRATION=1 is set.

    This keeps the default test run fast for unit tests. To run integration tests,
    set the environment variable RUN_INTEGRATION=1 before running pytest.
    """
    run_integration = os.environ.get("RUN_INTEGRATION", "0") == "1"
    if run_integration:
        return

    skip_marker = pytest.mark.skip(
        reason="Integration tests skipped by default. Set RUN_INTEGRATION=1 to run them."
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_marker)
