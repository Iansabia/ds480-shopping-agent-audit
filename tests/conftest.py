import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from harness.catalog import Catalog  # noqa: E402


@pytest.fixture(scope="session")
def cat():
    return Catalog()
