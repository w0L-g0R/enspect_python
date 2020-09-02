import os
import time
from pathlib import Path

import pytest

from src.enspect.aggregates.common import provinces
from src.enspect.models.dataset import DataSet
from src.enspect.models.workbook import Workbook
from src.enspect.paths import file_paths
from src.enspect.settings import set_pd_options
from tests.fixtures_eb import *
from tests.fixtures_IO import *
from tests.fixtures_nea import *


@pytest.fixture(scope="session")
def test_provinces():
    return provinces


set_pd_options()
TEST_USER = "WG"
SRC_ROOT = Path("src/dispat").resolve()
