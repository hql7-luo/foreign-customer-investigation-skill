from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents" / "skills" / "foreign-customer-investigation" / "scripts"
EXAMPLES = ROOT / "examples"
for path in (SCRIPTS, EXAMPLES):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from build_examples import make_report  # noqa: E402
from models import ReportLanguage  # noqa: E402


@pytest.fixture
def report_a():
    return make_report("a", ReportLanguage.ZH_CN)


@pytest.fixture
def report_b():
    return make_report("b", ReportLanguage.EN)


@pytest.fixture
def report_c():
    return make_report("c", ReportLanguage.BILINGUAL)


@pytest.fixture
def report_d():
    return make_report("d", ReportLanguage.EN)
