import sys
from pathlib import Path
import copy
import pytest
from fastapi.testclient import TestClient

# Make src/ importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import app as app_module

# baseline snapshot of activities to restore between tests
BASELINE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # restore the in-memory activities dict before each test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(BASELINE_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(BASELINE_ACTIVITIES))


@pytest.fixture
def client():
    with TestClient(app_module.app) as c:
        yield c
