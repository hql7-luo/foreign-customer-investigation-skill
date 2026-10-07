"""Rebuild small README visuals from the existing validated fictional fixture.

No browser, network, customer lookup or new scoring logic is involved. SVG text
and bar lengths come from the report model; the workflow documents SKILL.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [
    str(ROOT / ".agents/skills/foreign-customer-investigation/scripts"),
    str(ROOT / "examples"),
]
from build_examples import make_report  # noqa: E402
from models import InvestigationReport, ReportLanguage, derive_grade  # noqa: E402

SOURCE = ROOT / "examples/chinese-user-overseas-customer/FICTIONAL_Aurora_Printworks_investigation.json"
OUT = ROOT / "docs/visuals"
DIMENSIONS = ("authenticity", "business_fit", "purchase_signal", "purchase_potential", "contact_execution")


def wrap(value: str, limit: int) -> list[str]:
    """Wrap English at words and CJK at characters, without truncating facts."""
    lines, line, length = [], "", 0
    tokens = list(value) if any(unicodedata.east_asian_width(c) == "W" for c in value) else value.split(" ")
    separator = "" if len(tokens) == len(value) else " "
    for token in tokens:
        size = sum(2 if unicodedata.east_asian_width(c) == "W" else 1 for c in token)
        if line and length + size + len(separator) > limit:
            lines.append(line)
            line, length = "", 0
        line += (separator if line else "") + token
        length += size + len(separator)
    if line:
        lines.append(line)
    return lines


class SVG:
    def __init__(self, width: int, height: int, title: str):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">',
            f'<title id="title">{escape(title)}</title>',
            '<style>text{font-family:Arial,"PingFang SC","Microsoft YaHei",sans-serif;fill:#182c3c}.muted{fill:#536575}.accent{fill:#166b67}.bold{font-weight:700}</style>',
            f'<rect width="{width}" height="{height}" rx="24" fill="#f4f7f8"/>',
        ]

    def box(self, x, y, w, h, fill="#ffffff", stroke="#d6e0e5"):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}"/>')

    def text(self, x, y, value, size=28, cls="", anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def lines(self, x, y, value, limit, size=28, cls=""):
        lines = wrap(value, limit)
        for i, line in enumerate(lines):
            self.text(x, y + i * (size + 10), line, size, cls)
        return len(lines)

    def arrow(self, x, y):
        self.parts.append(f'<path d="M{x} {y}v20m-7-7 7 7 7-7" fill="none" stroke="#68818e" stroke-width="3"/>')

    def render(self):
        return "\n".join(self.parts + ["</svg>", ""])


def workflow(zh: bool) -> str:
    def t(en, cn):
        return cn if zh else en
    svg = SVG(900, 790, t("Customer investigation: input to decision and reports", "客户调查：从输入到开发决策与报告"))
    svg.text(44, 58, t("CUSTOMER INVESTIGATION WORKFLOW", "客户调查 · 核心业务流程"), 29, "bold")
    svg.box(40, 85, 820, 95)
    svg.text(65, 122, t("01  Input", "01  输入"), 31, "bold")
    svg.text(65, 159, t("Company name · Website · Business card · Inquiry", "公司名称 · 官网 · 名片 · 询盘信息"), 28, "muted")
    svg.arrow(450, 186)
    svg.box(40, 219, 390, 105)
    svg.text(65, 258, t("02  Collect evidence", "02  收集证据"), 30, "bold")
    svg.text(65, 295, t("Sources + evidence status", "来源 + 证据状态"), 26, "muted")
    svg.text(450, 279, "→", 35, "muted", "middle")
    svg.box(470, 219, 390, 105)
    svg.text(495, 258, t("03  Verify company", "03  核验公司"), 30, "bold")
    svg.text(495, 295, t("Entity + contact consistency", "主体 + 联系方式一致性"), 25, "muted")
    svg.arrow(450, 330)
    svg.box(40, 363, 820, 102)
    svg.text(65, 402, t("04  Assess the commercial opportunity", "04  判断商业机会"), 31, "bold")
    svg.text(65, 439, t("Customer type · Product fit · Purchase signals · Risk", "客户类型 · 产品匹配 · 采购信号 · 风险"), 27, "muted")
    svg.arrow(450, 471)
    svg.box(40, 504, 820, 110, "#e8f3f0", "#c1dbd3")
    svg.text(65, 549, t("05  Score 0–100 → Grade A / B / C / D", "05  0–100 分 → A / B / C / D 等级"), 31, "bold")
    svg.text(65, 586, t("Evidence-based grade caps → One priority action", "证据条件限制等级 → 一个最优先行动"), 27, "accent")
    svg.arrow(450, 620)
    svg.box(40, 653, 820, 92)
    svg.text(65, 690, t("06  Generate consistent reports", "06  生成一致的报告"), 31, "bold")
    svg.text(65, 725, "DOCX  /  XLSX  /  JSON", 29, "accent")
    svg.text(450, 776, t("Agent research + Python validation/export; evidence gaps remain explicit.", "Agent 研究 + Python 验证与导出；信息缺口明确保留。"), 21, "muted", "middle")
    return svg.render()


def result_card(report: InvestigationReport, zh: bool) -> str:
    def t(en, cn):
        return cn if zh else en
    svg = SVG(900, 1250, t("Fictional Aurora report preview and actual score breakdown", "虚构 Aurora 报告摘要与实际评分拆解"))
    svg.box(30, 28, 840, 42, "#fff2d7", "#e4cca0")
    svg.text(450, 56, t(report.fictional_notice, "虚构示例 — 不是真实公司或客户结果"), 24, "bold", "middle")
    svg.text(45, 115, report.customer.english_name, 31, "bold")
    svg.text(45, 151, t("Generated report summary", "生成报告摘要") + f"  ·  {report.investigation_date}", 24, "muted")
    svg.text(45, 245, report.scoring.total_score, 88, "bold")
    svg.text(169, 242, "/ 100", 30, "muted")
    svg.text(365, 235, f'{t("Grade", "等级")} {report.scoring.final_grade.value}', 48, "accent bold")
    grade_actions = {
        "A": ("Priority development", "优先开发"),
        "B": ("Active development", "主动开发"),
        "C": ("Low-cost follow-up", "低成本跟进"),
        "D": ("Defer", "暂缓开发"),
    }
    svg.text(365, 271, t(*grade_actions[report.scoring.final_grade.value]), 28, "accent")
    svg.text(45, 302, t("Development value: ", "开发价值：") + report.development_value, 25, "muted")

    rows = [
        (t("Customer type", "客户类型"), report.business_analysis.customer_type),
        (t("Purchase signals", "采购信号"), " / ".join(s.signal_type for s in report.purchase_signals)),
        (t("Product fit", "匹配产品"), " / ".join(report.recommended_products)),
        (t("Main risk", "主要风险"), report.maximum_risk),
    ]
    y = 344
    for label, value in rows:
        svg.text(45, y, label, 23, "muted")
        n = svg.lines(280, y, value, 42, 27, "bold")
        y += max(45, n * 37)
    action_y = max(545, y + 8)
    svg.box(30, action_y, 840, 132, "#e8f3f0", "#c1dbd3")
    svg.text(50, action_y + 33, t("RECOMMENDED NEXT ACTION", "建议下一步"), 23, "accent bold")
    n = svg.lines(50, action_y + 73, report.priority_action, 61, 28, "bold")
    assert n <= 2, "Increase the action panel height rather than truncating the source."
    bars_y = action_y + 185
    svg.text(45, bars_y, t("AUDITABLE SCORE BREAKDOWN", "可追溯评分拆解"), 28, "bold")
    svg.text(45, bars_y + 33, t("Points earned / dimension maximum", "已得分 / 该维度满分"), 23, "muted")
    for i, key in enumerate(DIMENSIONS):
        d = getattr(report.scoring, key)
        y = bars_y + 78 + i * 50
        svg.text(45, y, d.name, 27)
        svg.box(360, y - 21, 360, 22, "#dce6e8", "none")
        svg.box(360, y - 21, 360 * d.subtotal / d.max_score, 22, "#247a77", "none")
        svg.text(850, y, f"{d.subtotal} / {d.max_score}", 27, "bold", "end")
    y = bars_y + 332
    svg.text(45, y, t("Risk deduction", "风险扣分"), 27)
    svg.text(850, y, report.scoring.risk_deduction.subtotal, 28, "bold", "end")
    subtotal = sum(getattr(report.scoring, key).subtotal for key in DIMENSIONS)
    svg.text(45, y + 49, f"{subtotal} + ({report.scoring.risk_deduction.subtotal}) = {report.scoring.total_score}", 29, "accent bold")
    svg.text(45, y + 86, t("Grade also depends on evidence caps; high scores alone do not imply A.", "等级同时受证据条件限制；高分本身不代表 A。"), 23, "muted")
    svg.text(45, 1225, t("Source: validated Aurora example JSON + existing example generator (English).", "来源：已验证的 Aurora 示例 JSON；所有评分和叙述沿用现有示例。"), 21, "muted")
    return svg.render()


def build() -> dict[str, str]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    report_zh = InvestigationReport.model_validate(payload)
    generated_zh = make_report("a", ReportLanguage.ZH_CN)
    assert report_zh.model_dump(mode="json") == generated_zh.model_dump(mode="json"), "Committed fixture has drifted from its generator."
    report_en = make_report("a", ReportLanguage.EN)
    for key in DIMENSIONS:
        a, b = getattr(report_zh.scoring, key), getattr(report_en.scoring, key)
        assert [i.score for i in a.items] == [i.score for i in b.items]
        assert a.max_score == b.max_score
    assert report_zh.scoring.total_score == report_en.scoring.total_score
    assert derive_grade(report_zh) == derive_grade(report_en) == report_zh.scoring.final_grade
    outputs = {}
    for locale, report in (("en", report_en), ("zh", report_zh)):
        outputs[f"workflow-{locale}.svg"] = workflow(locale == "zh")
        outputs[f"result-{locale}.svg"] = result_card(report, locale == "zh")
    manifest = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "fictional_notice": report_zh.fictional_notice,
        "total_score": report_zh.scoring.total_score,
        "grade": report_zh.scoring.final_grade.value,
        "dimensions": {k: {"score": getattr(report_zh.scoring, k).subtotal, "maximum": getattr(report_zh.scoring, k).max_score} for k in DIMENSIONS},
        "risk_deduction": report_zh.scoring.risk_deduction.subtotal,
        "visual_sha256": {name: hashlib.sha256(value.encode()).hexdigest() for name, value in outputs.items()},
    }
    outputs["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed visuals differ from validated source data.")
    args = parser.parse_args()
    outputs = build()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, value in outputs.items():
        path = OUT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != value:
                raise SystemExit(f"Out-of-date visual: {path.relative_to(ROOT)}")
        else:
            path.write_text(value, encoding="utf-8")
    print(f"{'Verified' if args.check else 'Generated'} {len(outputs) - 1} source-derived visuals; score and grade reconciled.")


if __name__ == "__main__":
    main()
