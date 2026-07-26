"""Unified, language-neutral data model for every report output.

Narrative fields are authored in the requested report language. Stable enum values
remain English so JSON consumers can process reports without locale-specific logic.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_validator


class StrictModel(BaseModel):
    """Reject accidental fields so output drift is caught early."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ReportLanguage(str, Enum):
    ZH_CN = "zh-CN"
    EN = "en"
    BILINGUAL = "zh-CN+en"


class ReportMode(str, Enum):
    FULL = "full"
    SIMPLIFIED = "simplified"


class EvidenceStatus(str, Enum):
    CONFIRMED = "confirmed"
    PARTIALLY_CONFIRMED = "partially_confirmed"
    INFERRED = "inferred"
    CONFLICT = "conflict"
    NOT_FOUND = "not_found"


class Grade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Contact(StrictModel):
    name: str = ""
    original_name: str = ""
    job_title: str = ""
    phone: str = ""
    email: str = ""
    social_profile: str = ""

    @field_validator("phone")
    @classmethod
    def keep_international_prefix(cls, value: str) -> str:
        """Keep the user's country prefix; only trim surrounding whitespace."""

        return value.strip()


class Customer(StrictModel):
    legal_name: str
    trading_name: str = ""
    original_name: str = ""
    english_name: str = ""
    chinese_name: str = ""
    brand: str = ""
    country_code: str = Field(min_length=2, max_length=2)
    country_name: str = ""
    registration_number: str = ""
    tax_id: str = ""
    website: str = ""
    address: str = ""
    original_address: str = ""
    contact: Contact = Field(default_factory=Contact)

    @field_validator("country_code")
    @classmethod
    def uppercase_country_code(cls, value: str) -> str:
        return value.upper()


class Verification(StrictModel):
    legal_entity_status: EvidenceStatus
    business_registry_confirmed: bool = False
    registration_status: str = "Unable to confirm"
    website_status: EvidenceStatus = EvidenceStatus.NOT_FOUND
    email_domain_match: bool = False
    phone_verified: bool = False
    address_verified: bool = False
    contact_verified: bool = False
    information_consistent: bool = False
    cross_verified: bool = False
    authenticity_doubtful: bool = False
    generic_company_name: bool = False
    personal_contact_only: bool = False
    insufficient_normal_scoring: bool = False
    conflicts: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)


class BusinessAnalysis(StrictModel):
    customer_type: str
    main_business: str
    business_model: str = ""
    competition_environment: str = ""
    evidence_status: EvidenceStatus


class ProductionAndProcess(StrictModel):
    printing_processes: list[str] = Field(default_factory=list)
    application_scenarios: list[str] = Field(default_factory=list)
    equipment_models: list[str] = Field(default_factory=list)
    equipment_note: str = "No reliable public equipment model was found; confirm directly with the customer."
    evidence_status: EvidenceStatus


class SupplierAndImportRecords(StrictModel):
    cooperation_brands: list[str] = Field(default_factory=list)
    current_suppliers: list[str] = Field(default_factory=list)
    supplier_countries: list[str] = Field(default_factory=list)
    import_records: list[str] = Field(default_factory=list)
    summary: str = "No reliable public record was found."
    evidence_status: EvidenceStatus


class SalesChannels(StrictModel):
    channels: list[str] = Field(default_factory=list)
    market_scope: list[str] = Field(default_factory=list)
    summary: str
    evidence_status: EvidenceStatus


class CompanyScale(StrictModel):
    revenue: str = "No reliable public information was found."
    employee_count: str = "No reliable public information was found."
    capacity: str = "No reliable public information was found."
    operating_status: str = "Unable to confirm"
    summary: str = "No reliable public information was found."
    evidence_status: EvidenceStatus = EvidenceStatus.NOT_FOUND


class ProductRecommendation(StrictModel):
    customer_product_or_equipment: str
    printing_process: str
    specific_need: str
    recommended_product: str
    reason: str
    parameters_to_confirm: list[str] = Field(min_length=1)
    evidence_status: EvidenceStatus


class PurchaseSignal(StrictModel):
    signal_type: str
    detail: str
    explicit: bool = False
    evidence_status: EvidenceStatus
    source_ids: list[str] = Field(default_factory=list)


class FollowUpQuestion(StrictModel):
    priority: int = Field(ge=1)
    question: str
    reason: str
    customer_answer: str = ""
    subsequent_action: str = ""


class Risk(StrictModel):
    category: str
    risk: str
    deduction: int = Field(le=0, ge=-10)
    evidence_status: EvidenceStatus
    mitigation: str
    source_ids: list[str] = Field(default_factory=list)


class InvestigationItem(StrictModel):
    number: int = Field(ge=1, le=9)
    item: str
    core_finding: str
    evidence_status: EvidenceStatus
    source_ids: list[str] = Field(default_factory=list)
    needs_customer_confirmation: bool


class Source(StrictModel):
    source_id: str
    page_title: str
    url: str
    source_type: str
    access_date: date
    supports: str
    credibility: Literal["high", "medium", "low"]
    information_year: int | None = None
    is_core: bool = False

    @field_validator("url")
    @classmethod
    def require_full_url(cls, value: str) -> str:
        if not value.startswith(("https://", "http://")):
            raise ValueError("source URL must be a full http(s) URL")
        return value


class ScoreItem(StrictModel):
    name: str
    max_score: int = Field(gt=0)
    score: int = Field(ge=0)
    rationale: str
    evidence_status: EvidenceStatus

    @model_validator(mode="after")
    def score_does_not_exceed_maximum(self) -> "ScoreItem":
        if self.score > self.max_score:
            raise ValueError(f"{self.name}: score exceeds maximum")
        return self


class ScoreDimension(StrictModel):
    name: str
    max_score: int = Field(gt=0)
    items: list[ScoreItem]

    @computed_field
    @property
    def subtotal(self) -> int:
        return sum(item.score for item in self.items)

    @model_validator(mode="after")
    def subtotal_does_not_exceed_maximum(self) -> "ScoreDimension":
        if sum(item.max_score for item in self.items) != self.max_score:
            raise ValueError(f"{self.name}: item maxima do not equal dimension maximum")
        if self.subtotal > self.max_score:
            raise ValueError(f"{self.name}: subtotal exceeds dimension maximum")
        return self


class RiskScoreItem(StrictModel):
    name: str
    score: int = Field(le=0, ge=-10)
    rationale: str
    evidence_status: EvidenceStatus


class RiskDimension(StrictModel):
    name: str = "Risk deduction"
    items: list[RiskScoreItem] = Field(default_factory=list)

    @computed_field
    @property
    def subtotal(self) -> int:
        return max(-20, sum(item.score for item in self.items))

    @model_validator(mode="after")
    def deduction_does_not_exceed_cap(self) -> "RiskDimension":
        if sum(item.score for item in self.items) < -20:
            raise ValueError("risk deduction items may not total less than -20")
        return self


class Scoring(StrictModel):
    authenticity: ScoreDimension
    business_fit: ScoreDimension
    purchase_signal: ScoreDimension
    purchase_potential: ScoreDimension
    contact_execution: ScoreDimension
    risk_deduction: RiskDimension
    total_score: int = Field(ge=0, le=100)
    final_grade: Grade

    def calculated_total(self) -> int:
        positive = (
            self.authenticity.subtotal
            + self.business_fit.subtotal
            + self.purchase_signal.subtotal
            + self.purchase_potential.subtotal
            + self.contact_execution.subtotal
        )
        return max(0, min(100, positive + self.risk_deduction.subtotal))

    @model_validator(mode="after")
    def total_matches_details(self) -> "Scoring":
        if self.total_score != self.calculated_total():
            raise ValueError(
                f"total_score {self.total_score} does not match calculated total "
                f"{self.calculated_total()}"
            )
        return self


class InvestigationReport(StrictModel):
    investigation_date: date
    report_language: ReportLanguage
    mode: ReportMode
    fictional_notice: str = ""
    customer: Customer
    verification: Verification
    business_analysis: BusinessAnalysis
    production_and_process: ProductionAndProcess
    supplier_and_import_records: SupplierAndImportRecords
    sales_channels: SalesChannels
    company_scale: CompanyScale
    investigation_items: list[InvestigationItem]
    product_recommendations: list[ProductRecommendation] = Field(max_length=3)
    purchase_signals: list[PurchaseSignal] = Field(default_factory=list)
    follow_up_questions: list[FollowUpQuestion] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    scoring: Scoring
    conclusion: str
    development_value: str
    first_contact_focus: str
    evidence_gaps: list[str] = Field(default_factory=list)
    priority_action: str
    not_recommended_action: str
    maximum_risk: str
    sources: list[Source]

    @computed_field
    @property
    def recommended_products(self) -> list[str]:
        return [item.recommended_product for item in self.product_recommendations]

    @computed_field
    @property
    def core_sources(self) -> list[Source]:
        return [source for source in self.sources if source.is_core]

    @computed_field
    @property
    def explicit_purchase_signal(self) -> bool:
        return any(signal.explicit for signal in self.purchase_signals)

    @computed_field
    @property
    def information_completeness(self) -> int:
        weights = {
            EvidenceStatus.CONFIRMED: 2,
            EvidenceStatus.PARTIALLY_CONFIRMED: 1,
            EvidenceStatus.INFERRED: 0,
            EvidenceStatus.CONFLICT: 0,
            EvidenceStatus.NOT_FOUND: 0,
        }
        return sum(weights[item.evidence_status] for item in self.investigation_items)

    @model_validator(mode="after")
    def enforce_report_invariants(self) -> "InvestigationReport":
        numbers = [item.number for item in self.investigation_items]
        if sorted(numbers) != list(range(1, 10)):
            raise ValueError("investigation_items must contain each item number 1 through 9 once")
        core_count = len(self.core_sources)
        if core_count < 3 or core_count > 5:
            raise ValueError("each report must retain 3-5 core sources")
        if len({source.source_id for source in self.sources}) != len(self.sources):
            raise ValueError("source_id values must be unique")
        if self.risks and self.maximum_risk != most_severe_risk(self.risks):
            raise ValueError("maximum_risk must match the most severe listed risk")
        if should_use_simplified_mode(self) and self.mode != ReportMode.SIMPLIFIED:
            raise ValueError("information gaps require simplified mode")
        expected_grade = derive_grade(self)
        if self.scoring.final_grade != expected_grade:
            raise ValueError(
                f"final_grade {self.scoring.final_grade.value} does not match derived "
                f"grade {expected_grade.value}"
            )
        return self


class RankingEntry(StrictModel):
    rank: int = Field(ge=1)
    company_name: str
    final_grade: Grade
    total_score: int
    recommended_products: list[str]
    core_purchase_signal: str
    maximum_risk: str
    priority_action: str
    purchase_signal_score: int
    business_fit_score: int
    contact_execution_score: int
    purchase_potential_score: int
    information_completeness: int
    risk_deduction: int


def most_severe_risk(risks: list[Risk]) -> str:
    """Return a deterministic maximum-risk label."""

    if not risks:
        return "No confirmed material risk; verification gaps remain."
    return sorted(risks, key=lambda item: (item.deduction, item.risk))[0].risk


def should_use_simplified_mode(report: InvestigationReport) -> bool:
    """Apply every simplified-mode trigger from the specification."""

    missing_items = sum(
        item.evidence_status in {EvidenceStatus.NOT_FOUND, EvidenceStatus.CONFLICT}
        for item in report.investigation_items
    )
    verification = report.verification
    return any(
        (
            missing_items >= 5,
            not bool(report.customer.website),
            not verification.business_registry_confirmed,
            not verification.cross_verified,
            verification.generic_company_name,
            verification.personal_contact_only,
            verification.insufficient_normal_scoring,
        )
    )


def derive_grade(report: InvestigationReport) -> Grade:
    """Derive one legal grade from score bands plus all mandatory caps."""

    score = report.scoring.total_score
    severe_risk = any(
        risk.deduction <= -8
        and risk.category.lower() in {"sanctions", "compliance", "fraud", "entity", "payment"}
        for risk in report.risks
    )
    if severe_risk:
        return Grade.D
    if score < 40:
        return Grade.D

    if report.mode == ReportMode.SIMPLIFIED:
        return Grade.C
    if not report.customer.website and not report.verification.business_registry_confirmed:
        return Grade.C
    if score < 60:
        return Grade.C
    if score < 80:
        return Grade.B

    a_eligible = all(
        (
            report.explicit_purchase_signal,
            report.verification.business_registry_confirmed,
            report.verification.information_consistent,
            not report.verification.authenticity_doubtful,
            not severe_risk,
        )
    )
    return Grade.A if a_eligible else Grade.B


def rank_reports(reports: list[InvestigationReport]) -> list[RankingEntry]:
    """Return a strict, deterministic ranking with no tied rank numbers."""

    indexed = list(enumerate(reports))
    ordered = sorted(
        indexed,
        key=lambda pair: (
            -pair[1].scoring.purchase_signal.subtotal,
            -pair[1].scoring.business_fit.subtotal,
            -pair[1].scoring.contact_execution.subtotal,
            -pair[1].scoring.purchase_potential.subtotal,
            -pair[1].information_completeness,
            -pair[1].scoring.risk_deduction.subtotal,
            -pair[1].scoring.total_score,
            pair[1].customer.legal_name.casefold(),
            pair[0],
        ),
    )
    entries: list[RankingEntry] = []
    for rank, (_, report) in enumerate(ordered, start=1):
        signal = next(
            (item.detail for item in report.purchase_signals if item.explicit),
            report.purchase_signals[0].detail if report.purchase_signals else "No purchase signal confirmed",
        )
        entries.append(
            RankingEntry(
                rank=rank,
                company_name=report.customer.legal_name,
                final_grade=report.scoring.final_grade,
                total_score=report.scoring.total_score,
                recommended_products=report.recommended_products,
                core_purchase_signal=signal,
                maximum_risk=report.maximum_risk,
                priority_action=report.priority_action,
                purchase_signal_score=report.scoring.purchase_signal.subtotal,
                business_fit_score=report.scoring.business_fit.subtotal,
                contact_execution_score=report.scoring.contact_execution.subtotal,
                purchase_potential_score=report.scoring.purchase_potential.subtotal,
                information_completeness=report.information_completeness,
                risk_deduction=report.scoring.risk_deduction.subtotal,
            )
        )
    return entries


def score_dimension(
    name: str,
    definitions: list[tuple[str, int]],
    scores: list[int],
    rationales: list[str],
    statuses: list[EvidenceStatus] | None = None,
) -> ScoreDimension:
    """Convenience constructor used by examples and downstream agents."""

    if not (len(definitions) == len(scores) == len(rationales)):
        raise ValueError("definitions, scores, and rationales must have equal length")
    evidence = statuses or [EvidenceStatus.PARTIALLY_CONFIRMED] * len(definitions)
    if len(evidence) != len(definitions):
        raise ValueError("statuses must match definitions")
    items = [
        ScoreItem(
            name=item_name,
            max_score=maximum,
            score=score,
            rationale=rationale,
            evidence_status=status,
        )
        for (item_name, maximum), score, rationale, status in zip(
            definitions, scores, rationales, evidence, strict=True
        )
    ]
    return ScoreDimension(name=name, max_score=sum(maximum for _, maximum in definitions), items=items)


AUTHENTICITY_ITEMS = [
    ("Business registry", 6),
    ("Website and email", 4),
    ("Phone and address", 4),
    ("Contact authenticity", 3),
    ("Information consistency", 3),
]
BUSINESS_FIT_ITEMS = [
    ("Direct industry relevance", 10),
    ("Process and application fit", 8),
    ("Product entry feasibility", 7),
]
PURCHASE_SIGNAL_ITEMS = [
    ("Explicit inquiry or demand", 10),
    ("Sample, test, or quotation", 7),
    ("Parameters, quantity, or timing", 5),
    ("Ongoing communication or reply", 3),
]
PURCHASE_POTENTIAL_ITEMS = [
    ("Consumption frequency", 5),
    ("Production or channel scale", 5),
    ("Repeat purchase likelihood", 3),
    ("Alternative supply opportunity", 2),
]
CONTACT_EXECUTION_ITEMS = [
    ("Valid contact method", 5),
    ("Relevant contact role", 4),
    ("Reply status", 3),
    ("Clear next step", 3),
]
