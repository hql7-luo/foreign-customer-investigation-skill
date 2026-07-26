"""Generate the canonical machine-readable JSON report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .file_utils import ensure_output_dir, output_basename
    from .models import InvestigationReport
except ImportError:  # pragma: no cover
    from file_utils import ensure_output_dir, output_basename
    from models import InvestigationReport


def load_report(path: str | Path) -> InvestigationReport:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return InvestigationReport.model_validate(raw)


def generate_json(report: InvestigationReport, output_path: str | Path) -> Path:
    """Write UTF-8 JSON from the same model used by Word and Excel."""

    destination = Path(output_path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = report.model_dump(mode="json", exclude_computed_fields=True)
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", help="Validated investigation data")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    report = load_report(args.input_json)
    directory = ensure_output_dir(args.output_dir)
    path = directory / f"{output_basename(report)}_investigation.json"
    print(generate_json(report, path))


if __name__ == "__main__":
    main()
