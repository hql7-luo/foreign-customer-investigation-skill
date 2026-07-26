from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from openpyxl import load_workbook


EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
PHONE = re.compile(r"\+[0-9][0-9 ()-]{7,}[0-9]")
SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def _artifact_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        document = Document(path)
        chunks = [paragraph.text for paragraph in document.paragraphs]
        for table in document.tables:
            for row in table.rows:
                chunks.extend(cell.text for cell in row.cells)
        return "\n".join(chunks)
    if path.suffix.lower() == ".xlsx":
        workbook = load_workbook(path, data_only=False, read_only=False)
        return "\n".join(
            str(cell.value)
            for sheet in workbook.worksheets
            for row in sheet.iter_rows()
            for cell in row
            if cell.value is not None
        )
    return path.read_text(encoding="utf-8", errors="ignore")


def test_public_repository_contains_only_fictional_contact_data():
    root = Path(__file__).resolve().parents[1]
    files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix.lower() in {".py", ".md", ".json", ".txt", ".docx", ".xlsx", ""}
    ]
    corpus = "\n".join(_artifact_text(path) for path in files)

    for pattern in SECRET_PATTERNS:
        assert not pattern.search(corpus), f"possible secret detected: {pattern.pattern}"

    domains = {match.group(1).lower() for match in EMAIL.finditer(corpus)}
    assert all(domain.endswith(".example") or domain == "example.com" for domain in domains)

    phones = {match.group(0) for match in PHONE.finditer(corpus)}
    assert all(phone.startswith("+999") for phone in phones)
    assert not any(path.name == "客户背景调查提示词.docx" for path in files)


def test_every_binary_example_is_visibly_fictional():
    root = Path(__file__).resolve().parents[1]
    artifacts = [
        path
        for base in (
            root / "examples",
            root / ".agents" / "skills" / "foreign-customer-investigation" / "templates",
        )
        for path in base.rglob("*")
        if path.suffix.lower() in {".docx", ".xlsx"}
    ]
    assert artifacts
    for artifact in artifacts:
        assert "FICTIONAL EXAMPLE — NOT A REAL COMPANY" in _artifact_text(artifact)
