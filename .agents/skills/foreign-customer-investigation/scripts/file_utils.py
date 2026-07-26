"""Safe filenames and shared language helpers."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

try:
    from .models import EvidenceStatus, InvestigationReport, ReportLanguage
except ImportError:  # pragma: no cover - supports direct script execution
    from models import EvidenceStatus, InvestigationReport, ReportLanguage


INVALID_FILENAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def safe_filename(value: str, fallback: str = "customer") -> str:
    """Create a cross-platform filename without changing document titles."""

    normalized = unicodedata.normalize("NFKC", value).strip()
    cleaned = INVALID_FILENAME.sub("_", normalized)
    cleaned = re.sub(r"\s+", "_", cleaned).strip(" ._")
    return cleaned[:120] or fallback


def output_basename(report: InvestigationReport) -> str:
    preferred = report.customer.english_name or report.customer.legal_name
    return safe_filename(preferred)


def ensure_output_dir(path: str | Path) -> Path:
    directory = Path(path).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def localized(language: ReportLanguage, zh: str, en: str) -> str:
    if language == ReportLanguage.ZH_CN:
        return zh
    if language == ReportLanguage.EN:
        return en
    return f"{zh} / {en}"


def evidence_label(status: EvidenceStatus, language: ReportLanguage) -> str:
    labels = {
        EvidenceStatus.CONFIRMED: ("【已确认】", "[Confirmed]"),
        EvidenceStatus.PARTIALLY_CONFIRMED: ("【部分确认】", "[Partially confirmed]"),
        EvidenceStatus.INFERRED: ("【推测】", "[Inference]"),
        EvidenceStatus.CONFLICT: ("【信息冲突】", "[Conflicting information]"),
        EvidenceStatus.NOT_FOUND: ("【未找到】", "[Not found]"),
    }
    zh, en = labels[status]
    return localized(language, zh, en)


def join_items(items: list[str], language: ReportLanguage) -> str:
    if not items:
        return localized(
            language,
            "未找到公开可靠记录",
            "No reliable public record was found",
        )
    separator = "；" if language != ReportLanguage.EN else "; "
    return separator.join(items)
