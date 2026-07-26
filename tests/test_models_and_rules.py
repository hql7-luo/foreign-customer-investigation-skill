from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from build_examples import FICTIONAL_NOTICE, make_report
from models import (
    EvidenceStatus,
    Grade,
    InvestigationReport,
    ReportLanguage,
    ReportMode,
    RiskScoreItem,
    derive_grade,
    rank_reports,
)
from validate_report import validate_rankings, validate_report


def test_complete_explicit_inquiry_case_is_a(report_a):
    assert report_a.scoring.final_grade == Grade.A
    assert report_a.scoring.total_score == 97
    assert report_a.explicit_purchase_signal
    assert validate_report(report_a).passed


def test_real_customer_without_purchase_signal_is_b(report_b):
    assert report_b.scoring.final_grade == Grade.B
    assert not report_b.explicit_purchase_signal
    assert report_b.scoring.purchase_signal.subtotal <= 5
    assert validate_report(report_b).passed


def test_incomplete_customer_is_c(report_c):
    assert report_c.scoring.final_grade == Grade.C
    assert report_c.scoring.total_score == 40
    assert report_c.mode == ReportMode.SIMPLIFIED


def test_high_risk_customer_is_d(report_d):
    assert report_d.scoring.final_grade == Grade.D
    assert report_d.scoring.risk_deduction.subtotal == -8
    assert derive_grade(report_d) == Grade.D


def test_simplified_mode_trigger_cannot_be_ignored(report_c):
    payload = report_c.model_dump(mode="json", exclude_computed_fields=True)
    payload["mode"] = "full"
    with pytest.raises(ValidationError, match="simplified mode"):
        InvestigationReport.model_validate(payload)


def test_a_grade_requires_explicit_signal(report_a):
    payload = report_a.model_dump(mode="json", exclude_computed_fields=True)
    for signal in payload["purchase_signals"]:
        signal["explicit"] = False
    with pytest.raises(ValidationError, match="derived grade B"):
        InvestigationReport.model_validate(payload)


def test_illegal_grade_modifier_rejected(report_b):
    payload = report_b.model_dump(mode="json", exclude_computed_fields=True)
    payload["scoring"]["final_grade"] = "B+"
    with pytest.raises(ValidationError):
        InvestigationReport.model_validate(payload)


def test_score_item_upper_bound_rejected(report_a):
    payload = report_a.model_dump(mode="json", exclude_computed_fields=True)
    payload["scoring"]["authenticity"]["items"][0]["score"] = 7
    with pytest.raises(ValidationError, match="score exceeds maximum"):
        InvestigationReport.model_validate(payload)


def test_total_score_lower_bound_rejected(report_a):
    payload = report_a.model_dump(mode="json", exclude_computed_fields=True)
    payload["scoring"]["total_score"] = -1
    with pytest.raises(ValidationError):
        InvestigationReport.model_validate(payload)


def test_risk_deduction_cap_rejected(report_d):
    payload = report_d.model_dump(mode="json", exclude_computed_fields=True)
    payload["scoring"]["risk_deduction"]["items"] = [
        {
            "name": "Risk 1",
            "score": -10,
            "rationale": "Fictional test",
            "evidence_status": "confirmed",
        },
        {
            "name": "Risk 2",
            "score": -10,
            "rationale": "Fictional test",
            "evidence_status": "confirmed",
        },
        {
            "name": "Risk 3",
            "score": -1,
            "rationale": "Fictional test",
            "evidence_status": "confirmed",
        },
    ]
    with pytest.raises(ValidationError, match="less than -20"):
        InvestigationReport.model_validate(payload)


def test_recommendations_cannot_exceed_three(report_a):
    payload = report_a.model_dump(mode="json", exclude_computed_fields=True)
    item = payload["product_recommendations"][0]
    payload["product_recommendations"] = [item, item, item, item]
    with pytest.raises(ValidationError):
        InvestigationReport.model_validate(payload)


def test_core_sources_must_be_three_to_five(report_a):
    payload = report_a.model_dump(mode="json", exclude_computed_fields=True)
    payload["sources"] = payload["sources"][:2]
    with pytest.raises(ValidationError, match="3-5 core sources"):
        InvestigationReport.model_validate(payload)


def test_chinese_input_and_output_case():
    report = make_report("a", ReportLanguage.ZH_CN)
    assert report.report_language == ReportLanguage.ZH_CN
    assert "综合得分97分" in report.conclusion


def test_english_input_and_output_case():
    report = make_report("b", ReportLanguage.EN)
    assert report.report_language == ReportLanguage.EN
    assert "final grade is B" in report.conclusion


def test_chinese_customer_case(report_b):
    assert report_b.customer.country_code == "CN"
    assert report_b.customer.original_name == "虚构远景包装技术有限公司"


def test_overseas_customer_case(report_a):
    assert report_a.customer.country_code == "PL"
    assert report_a.customer.legal_name.startswith("FICTIONAL")


def test_mixed_language_case():
    report = make_report("a", ReportLanguage.BILINGUAL)
    assert report.report_language == ReportLanguage.BILINGUAL
    assert " / " in report.investigation_items[0].item


def test_batch_ranking_has_no_ties(report_a, report_b, report_c):
    entries = rank_reports([report_c, report_b, report_a])
    assert [entry.rank for entry in entries] == [1, 2, 3]
    assert [entry.final_grade for entry in entries] == [Grade.A, Grade.B, Grade.C]
    assert validate_rankings(entries).passed


def test_identical_scores_still_receive_unique_ranks(report_b):
    clone = InvestigationReport.model_validate(
        report_b.model_dump(mode="json", exclude_computed_fields=True)
    )
    entries = rank_reports([report_b, clone])
    assert [entry.rank for entry in entries] == [1, 2]


def test_all_public_examples_carry_fictional_notice(report_a, report_b, report_c, report_d):
    assert all(
        report.fictional_notice == FICTIONAL_NOTICE
        for report in (report_a, report_b, report_c, report_d)
    )


def test_phone_country_prefix_is_preserved(report_a):
    payload = json.loads(
        json.dumps(
            report_a.model_dump(mode="json", exclude_computed_fields=True),
            ensure_ascii=False,
        )
    )
    restored = InvestigationReport.model_validate(payload)
    assert restored.customer.contact.phone.startswith("+999")
