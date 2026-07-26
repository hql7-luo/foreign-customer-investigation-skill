"""Build all public examples from conspicuously fictional data."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "foreign-customer-investigation"
SCRIPTS = SKILL / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_docx import generate_docx  # noqa: E402
from generate_json import generate_json  # noqa: E402
from generate_xlsx import generate_xlsx  # noqa: E402
from models import (  # noqa: E402
    AUTHENTICITY_ITEMS,
    BUSINESS_FIT_ITEMS,
    CONTACT_EXECUTION_ITEMS,
    PURCHASE_POTENTIAL_ITEMS,
    PURCHASE_SIGNAL_ITEMS,
    BusinessAnalysis,
    CompanyScale,
    Contact,
    Customer,
    EvidenceStatus,
    FollowUpQuestion,
    Grade,
    InvestigationItem,
    InvestigationReport,
    ProductionAndProcess,
    ProductRecommendation,
    PurchaseSignal,
    ReportLanguage,
    ReportMode,
    Risk,
    RiskDimension,
    RiskScoreItem,
    SalesChannels,
    Scoring,
    Source,
    SupplierAndImportRecords,
    Verification,
    rank_reports,
    score_dimension,
)


FICTIONAL_NOTICE = "FICTIONAL EXAMPLE — NOT A REAL COMPANY"
EXAMPLE_DATE = date(2026, 7, 26)


def text(language: ReportLanguage, zh: str, en: str) -> str:
    if language == ReportLanguage.ZH_CN:
        return zh
    if language == ReportLanguage.EN:
        return en
    return f"{zh} / {en}"


def _customer(case: str) -> Customer:
    if case == "a":
        return Customer(
            legal_name="FICTIONAL Aurora Printworks Sp. z o.o.",
            trading_name="FICTIONAL Aurora Print",
            original_name="FICTIONAL Aurora Printworks Sp. z o.o.",
            english_name="FICTIONAL Aurora Printworks",
            chinese_name="虚构极光印刷有限公司",
            brand="FICTIONAL Aurora",
            country_code="PL",
            country_name="Poland",
            registration_number="FICTIONAL-PL-000001",
            tax_id="FICTIONAL-TAX-000001",
            website="https://aurora-print.example",
            address="1 Fictional Avenue, Example City, Poland",
            original_address="1 Fictional Avenue, Example City, Polska",
            contact=Contact(
                name="Maya Example",
                original_name="Maya Example",
                job_title="Purchasing Manager",
                phone="+999 000 000 001",
                email="maya.example@aurora-print.example",
            ),
        )
    if case == "b":
        return Customer(
            legal_name="虚构远景包装技术有限公司",
            trading_name="虚构远景包装",
            original_name="虚构远景包装技术有限公司",
            english_name="FICTIONAL Horizon Packaging Technology Co., Ltd.",
            chinese_name="虚构远景包装技术有限公司",
            brand="FICTIONAL Horizon",
            country_code="CN",
            country_name="China",
            registration_number="FICTIONAL-CN-000002",
            tax_id="FICTIONAL-USCC-000002",
            website="https://fictional-horizon.example",
            address="中国示例省虚构市示例路2号（虚构地址）",
            original_address="中国示例省虚构市示例路2号（虚构地址）",
            contact=Contact(
                name="Alex Example",
                original_name="Alex Example",
                job_title="Operations Manager",
                phone="+999 000 000 002",
                email="alex.example@fictional-horizon.example",
            ),
        )
    if case == "c":
        return Customer(
            legal_name="FICTIONAL Global Print",
            trading_name="FICTIONAL Global Print",
            original_name="شركة الطباعة العالمية الخيالية",
            english_name="FICTIONAL Global Print",
            chinese_name="虚构环球印刷",
            country_code="AE",
            country_name="United Arab Emirates",
            registration_number="",
            tax_id="",
            website="",
            address="",
            original_address="",
            contact=Contact(
                name="Fictional Contact",
                original_name="جهة اتصال خيالية",
                job_title="",
                phone="+999 000 000 003",
                email="fictional.contact@example.com",
            ),
        )
    return Customer(
        legal_name="FICTIONAL Red Flag Equipment Ltd.",
        trading_name="FICTIONAL Red Flag Equipment",
        original_name="FICTIONAL Red Flag Equipment Ltd.",
        english_name="FICTIONAL Red Flag Equipment",
        chinese_name="虚构红旗设备有限公司",
        brand="FICTIONAL Red Flag",
        country_code="GB",
        country_name="United Kingdom",
        registration_number="FICTIONAL-GB-000004",
        tax_id="FICTIONAL-TAX-000004",
        website="https://red-flag-equipment.example",
        address="4 Fictional Works, Example Town, United Kingdom",
        original_address="4 Fictional Works, Example Town, United Kingdom",
        contact=Contact(
            name="Jordan Example",
            original_name="Jordan Example",
            job_title="Sales Agent",
            phone="+999 000 000 004",
            email="jordan.example@red-flag-equipment.example",
        ),
    )


def _sources(case: str, customer: Customer, language: ReportLanguage) -> list[Source]:
    stem = f"fictional-{case}"
    return [
        Source(
            source_id="S1",
            page_title=text(language, "虚构官方工商记录", "Fictional official registry record"),
            url=f"https://registry.example/{stem}",
            source_type=text(language, "官方工商示例", "Official registry example"),
            access_date=EXAMPLE_DATE,
            supports=text(language, "主体状态（仅虚构测试）", "Entity status (fictional test only)"),
            credibility="high",
            information_year=2026,
            is_core=True,
        ),
        Source(
            source_id="S2",
            page_title=text(language, "虚构公司业务页面", "Fictional company business page"),
            url=f"https://company.example/{stem}/business",
            source_type=text(language, "公司官网示例", "Company website example"),
            access_date=EXAMPLE_DATE,
            supports=text(language, "对外宣传业务与工艺", "Published business and process"),
            credibility="medium",
            information_year=2026,
            is_core=True,
        ),
        Source(
            source_id="S3",
            page_title=text(language, "虚构地图记录", "Fictional map record"),
            url=f"https://maps.example/{stem}",
            source_type=text(language, "地图示例", "Map example"),
            access_date=EXAMPLE_DATE,
            supports=text(language, "地址与电话交叉验证", "Address and phone cross-check"),
            credibility="medium",
            information_year=2026,
            is_core=True,
        ),
        Source(
            source_id="S4",
            page_title=text(language, "虚构展会目录", "Fictional exhibition directory"),
            url=f"https://exhibition.example/{stem}",
            source_type=text(language, "展会示例", "Exhibition example"),
            access_date=EXAMPLE_DATE,
            supports=text(language, "业务类型与联系人线索", "Business type and contact clue"),
            credibility="medium",
            information_year=2025,
            is_core=True,
        ),
    ]


def _investigation_items(
    language: ReportLanguage,
    statuses: list[EvidenceStatus],
    case: str,
) -> list[InvestigationItem]:
    names = [
        ("公司主体与联系人真实性", "Company entity and contact authenticity"),
        ("主营业务、客户类型与竞争环境", "Main business, customer type, and competition"),
        ("生产设备、印刷工艺与应用场景", "Equipment, printing process, and applications"),
        ("现有供应商、合作品牌与进口记录", "Suppliers, brands, and import records"),
        ("销售渠道与市场范围", "Sales channels and market scope"),
        ("公司规模、产能与经营状态", "Scale, capacity, and operating status"),
        ("产品匹配与推荐产品", "Product fit and recommendations"),
        ("采购信号、采购频率与跟进时间", "Purchase signals, frequency, and timing"),
        ("采购痛点、风险与切入方案", "Pain points, risks, and entry approach"),
    ]
    findings_by_case = {
        "a": [
            ("工商示例、官网与地图信息一致；联系人有业务往来记录。", "Fictional registry, website, and map agree; the contact has direct correspondence."),
            ("纸盒印刷生产商，主营高端短单包装。", "Folding-carton printer focused on short-run premium packaging."),
            ("官网示例显示单张纸UV胶印；设备型号为虚构测试信息。", "The fictional website shows sheetfed UV offset; the equipment model is fictional test data."),
            ("未找到公开可靠的现用品牌、供应商或进口记录。", "No reliable public current-brand, supplier, or import record was found."),
            ("官网示例显示直销本地品牌客户；范围需确认。", "The fictional website presents direct sales to local brands; scope needs confirmation."),
            ("未找到可靠的营收、员工人数或产能信息。", "No reliable revenue, employee, or capacity information was found."),
            ("UV油墨和橡皮布与已确认工艺匹配。", "UV ink and blankets fit the confirmed process."),
            ("已明确询价并要求寄送测试样品。", "The customer made a clear inquiry and requested test samples."),
            ("最大不确定性是付款条款；先确认测试参数。", "Payment terms are the main uncertainty; confirm test parameters first."),
        ],
        "b": [
            ("工商示例与官网主体一致，联系人职位仅部分确认。", "The fictional registry and website entity agree; the contact role is partly confirmed."),
            ("中国纸包装生产企业，存在胶印耗材应用。", "A Chinese paper-packaging producer with offset-consumable applications."),
            ("可确认胶印场景，未找到公开设备型号。", "Offset use is supported; no public equipment model was found."),
            ("未找到公开可靠的供应商、品牌或进口记录。", "No reliable public supplier, brand, or import record was found."),
            ("官网示例显示本地B2B直销。", "The fictional website presents domestic B2B direct sales."),
            ("未找到可靠的营收、员工人数或产能信息。", "No reliable revenue, employee, or capacity information was found."),
            ("胶印油墨和印版具有条件匹配。", "Offset ink and printing plates are conditionally matched."),
            ("仅索要普通目录并保持回复，暂无明确询价。", "Only a general catalog was requested; replies continue but no explicit inquiry exists."),
            ("需先确认设备、规格和采购时间。", "Confirm equipment, specification, and purchase timing first."),
        ],
        "c": [
            ("仅有个人邮箱和电话，主体无法确认。", "Only a personal email and phone are available; the entity cannot be confirmed."),
            ("名称暗示印刷业务，但无法确认客户类型。", "The name suggests printing, but the customer type cannot be confirmed."),
            ("未找到公开设备型号或可靠工艺信息。", "No public equipment model or reliable process information was found."),
            ("未找到公开可靠记录。", "No reliable public record was found."),
            ("未找到可靠公开信息。", "No reliable public information was found."),
            ("营收、员工、产能和经营状态均无法确认。", "Revenue, employees, capacity, and operating status cannot be confirmed."),
            ("仅可条件性考虑胶印油墨，需先确认工艺。", "Offset ink is only a conditional option pending process confirmation."),
            ("未发现明确采购信号。", "No explicit purchase signal was identified."),
            ("最大风险是主体无法确认；仅建议低成本核实。", "The maximum risk is an unconfirmed entity; use low-cost verification only."),
        ],
        "d": [
            ("工商主体可确认，但付款主体与注册主体冲突。", "The registered entity is confirmed, but the payment beneficiary conflicts with it."),
            ("设备贸易业务部分确认，与耗材仅弱匹配。", "Equipment trading is partly confirmed; consumable fit is weak."),
            ("未找到公开设备型号。", "No public equipment model was found."),
            ("未找到公开可靠的供应商或进口记录。", "No reliable public supplier or import record was found."),
            ("公开页面仅显示有限本地销售线索。", "Public pages show limited local-sales clues."),
            ("未找到可靠的规模或产能信息。", "No reliable scale or capacity information was found."),
            ("缺少工艺参数，不建议现阶段推荐具体产品。", "Process parameters are missing; no specific product should be recommended now."),
            ("未发现明确采购信号。", "No explicit purchase signal was identified."),
            ("付款受益人严重冲突，暂缓开发。", "A serious payment-beneficiary conflict requires deferral."),
        ],
    }
    items = []
    for index, ((zh_name, en_name), (zh_finding, en_finding), status) in enumerate(
        zip(names, findings_by_case[case], statuses, strict=True), start=1
    ):
        source_ids = ["S1", "S2"] if status != EvidenceStatus.NOT_FOUND else []
        items.append(
            InvestigationItem(
                number=index,
                item=text(language, zh_name, en_name),
                core_finding=text(language, zh_finding, en_finding),
                evidence_status=status,
                source_ids=source_ids,
                needs_customer_confirmation=status != EvidenceStatus.CONFIRMED,
            )
        )
    return items


def _recommendations(case: str, language: ReportLanguage) -> list[ProductRecommendation]:
    if case == "a":
        rows = [
            (
                "纸盒/虚构FP-740设备",
                "Folding cartons / fictional FP-740 press",
                "UV胶印",
                "UV offset",
                "纸张与覆膜纸盒的附着、固化和耐磨",
                "Adhesion, curing, and rub resistance on paper/laminated cartons",
                "UV油墨",
                "UV ink",
                "与公开展示的UV胶印应用直接匹配",
                "Direct fit with the publicly presented UV-offset application",
                ["灯型与波长", "承印物", "色组", "固化速度"],
                ["Lamp type and wavelength", "Substrate", "Color set", "Curing speed"],
            ),
            (
                "纸盒/虚构FP-740设备",
                "Folding cartons / fictional FP-740 press",
                "UV胶印",
                "UV offset",
                "稳定转印与周期性更换",
                "Stable transfer and recurring replacement",
                "UV兼容橡皮布",
                "UV-compatible blankets",
                "橡皮布属于与设备尺寸直接相关的维护耗材",
                "Blankets are model-size-dependent maintenance consumables",
                ["滚筒尺寸", "厚度", "背衬", "当前品牌"],
                ["Cylinder dimensions", "Thickness", "Backing", "Current brand"],
            ),
        ]
    elif case == "b":
        rows = [
            (
                "纸盒",
                "Paper cartons",
                "胶印",
                "Offset",
                "常规四色印刷",
                "Conventional four-color printing",
                "胶印油墨",
                "Offset ink",
                "与已确认的胶印应用匹配，但需测试",
                "Fits the confirmed offset application, subject to testing",
                ["设备型号", "纸张", "色彩标准", "月度用量"],
                ["Press model", "Paper", "Color standard", "Monthly requirement"],
            ),
            (
                "纸盒",
                "Paper cartons",
                "胶印",
                "Offset",
                "制版与重复订单",
                "Plate making and repeat jobs",
                "印版",
                "Printing plates",
                "可作为第二切入点，规格尚未确认",
                "A possible second entry point; size is unconfirmed",
                ["版材尺寸", "制版机", "分辨率", "当前品牌"],
                ["Plate size", "Platesetter", "Resolution", "Current brand"],
            ),
        ]
    elif case == "c":
        rows = [
            (
                "无法确认",
                "Unable to confirm",
                "推测为胶印",
                "Offset inferred",
                "需先确认实际工艺",
                "Actual process must be confirmed first",
                "胶印油墨（条件性）",
                "Offset ink (conditional)",
                "仅由公司名称作弱推测，不可直接报价",
                "Weakly inferred from the name; do not quote yet",
                ["公司主体", "设备型号", "承印物", "具体需求"],
                ["Legal entity", "Press model", "Substrate", "Specific need"],
            )
        ]
    else:
        return []
    recommendations = []
    for row in rows:
        (
            zh_customer,
            en_customer,
            zh_process,
            en_process,
            zh_need,
            en_need,
            zh_product,
            en_product,
            zh_reason,
            en_reason,
            zh_params,
            en_params,
        ) = row
        recommendations.append(
            ProductRecommendation(
                customer_product_or_equipment=text(language, zh_customer, en_customer),
                printing_process=text(language, zh_process, en_process),
                specific_need=text(language, zh_need, en_need),
                recommended_product=text(language, zh_product, en_product),
                reason=text(language, zh_reason, en_reason),
                parameters_to_confirm=[
                    text(language, zh_value, en_value)
                    for zh_value, en_value in zip(zh_params, en_params, strict=True)
                ],
                evidence_status=(
                    EvidenceStatus.INFERRED if case == "c" else EvidenceStatus.PARTIALLY_CONFIRMED
                ),
            )
        )
    return recommendations


def _score(case: str, language: ReportLanguage) -> Scoring:
    configurations = {
        "a": (
            [6, 4, 4, 3, 3],
            [10, 8, 7],
            [10, 7, 5, 3],
            [5, 4, 3, 2],
            [5, 4, 3, 3],
            [-2],
            97,
            Grade.A,
        ),
        "b": (
            [6, 4, 3, 2, 3],
            [10, 6, 6],
            [0, 0, 0, 3],
            [4, 4, 3, 1],
            [5, 3, 2, 2],
            [-1],
            66,
            Grade.B,
        ),
        "c": (
            [3, 1, 1, 1, 2],
            [8, 3, 4],
            [0, 0, 0, 1],
            [4, 1, 2, 1],
            [4, 2, 1, 2],
            [-1],
            40,
            Grade.C,
        ),
        "d": (
            [6, 3, 3, 1, 1],
            [6, 3, 3],
            [0, 0, 0, 1],
            [2, 2, 1, 0],
            [3, 1, 1, 0],
            [-8],
            29,
            Grade.D,
        ),
    }
    auth, fit, signal, potential, contact, risk, total, grade = configurations[case]

    def rationales(definitions: list[tuple[str, int]]) -> list[str]:
        return [
            text(
                language,
                f"依据虚构测试证据逐项评分：{name}",
                f"Scored from fictional test evidence: {name}",
            )
            for name, _ in definitions
        ]

    risk_name = text(
        language,
        "付款条款未确认" if case == "a" else
        "采购信息不完整" if case == "b" else
        "主体信息不足" if case == "c" else
        "付款受益人冲突",
        "Payment terms unverified" if case == "a" else
        "Incomplete purchasing information" if case == "b" else
        "Insufficient entity information" if case == "c" else
        "Payment-beneficiary conflict",
    )
    return Scoring(
        authenticity=score_dimension(
            text(language, "客户真实性", "Authenticity"),
            AUTHENTICITY_ITEMS,
            auth,
            rationales(AUTHENTICITY_ITEMS),
        ),
        business_fit=score_dimension(
            text(language, "业务匹配度", "Business fit"),
            BUSINESS_FIT_ITEMS,
            fit,
            rationales(BUSINESS_FIT_ITEMS),
        ),
        purchase_signal=score_dimension(
            text(language, "采购信号", "Purchase signal"),
            PURCHASE_SIGNAL_ITEMS,
            signal,
            rationales(PURCHASE_SIGNAL_ITEMS),
        ),
        purchase_potential=score_dimension(
            text(language, "采购潜力", "Purchase potential"),
            PURCHASE_POTENTIAL_ITEMS,
            potential,
            rationales(PURCHASE_POTENTIAL_ITEMS),
        ),
        contact_execution=score_dimension(
            text(language, "联系可执行性", "Contact execution"),
            CONTACT_EXECUTION_ITEMS,
            contact,
            rationales(CONTACT_EXECUTION_ITEMS),
        ),
        risk_deduction=RiskDimension(
            name=text(language, "风险扣分", "Risk deduction"),
            items=[
                RiskScoreItem(
                    name=risk_name,
                    score=risk[0],
                    rationale=text(
                        language,
                        "按虚构案例中的已知风险扣分。",
                        "Deducted from the known risk in the fictional case.",
                    ),
                    evidence_status=(
                        EvidenceStatus.CONFLICT if case == "d" else EvidenceStatus.PARTIALLY_CONFIRMED
                    ),
                )
            ],
        ),
        total_score=total,
        final_grade=grade,
    )


def make_report(
    case: str,
    language: ReportLanguage = ReportLanguage.ZH_CN,
) -> InvestigationReport:
    if case not in {"a", "b", "c", "d"}:
        raise ValueError("case must be a, b, c, or d")
    customer = _customer(case)
    statuses = {
        "a": [
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
        ],
        "b": [
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
        ],
        "c": [
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.INFERRED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.INFERRED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.CONFLICT,
        ],
        "d": [
            EvidenceStatus.CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.PARTIALLY_CONFIRMED,
            EvidenceStatus.NOT_FOUND,
            EvidenceStatus.CONFLICT,
        ],
    }[case]
    mode = ReportMode.SIMPLIFIED if case == "c" else ReportMode.FULL
    verification = Verification(
        legal_entity_status=(
            EvidenceStatus.PARTIALLY_CONFIRMED if case == "c" else EvidenceStatus.CONFIRMED
        ),
        business_registry_confirmed=case != "c",
        registration_status=text(
            language,
            "无法确认" if case == "c" else "已确认（虚构测试）",
            "Unable to confirm" if case == "c" else "Confirmed (fictional test)",
        ),
        website_status=(
            EvidenceStatus.NOT_FOUND if case == "c" else EvidenceStatus.CONFIRMED
        ),
        email_domain_match=case != "c",
        phone_verified=case in {"a", "b", "d"},
        address_verified=case in {"a", "b", "d"},
        contact_verified=case == "a",
        information_consistent=case in {"a", "b"},
        cross_verified=case in {"a", "b", "d"},
        authenticity_doubtful=case in {"c", "d"},
        generic_company_name=case == "c",
        personal_contact_only=case == "c",
        insufficient_normal_scoring=case == "c",
        conflicts=(
            [text(language, "付款受益人与注册主体冲突", "Payment beneficiary conflicts with the registered entity")]
            if case == "d"
            else []
        ),
        findings=[
            text(
                language,
                "主体信息来自完全虚构的公开来源示例。",
                "Entity information comes from entirely fictional public-source examples.",
            )
        ],
    )

    risk_details = {
        "a": (
            "payment",
            "付款条款尚未核实",
            "Payment terms have not been verified",
            -2,
        ),
        "b": (
            "commercial",
            "采购数量、预算和时间不明确",
            "Quantity, budget, and timing are unclear",
            -1,
        ),
        "c": (
            "entity",
            "客户主体无法确认",
            "The customer entity cannot be confirmed",
            -1,
        ),
        "d": (
            "payment",
            "付款受益人与注册主体严重冲突",
            "The payment beneficiary materially conflicts with the registered entity",
            -8,
        ),
    }[case]
    category, zh_risk, en_risk, deduction = risk_details
    risk = Risk(
        category=category,
        risk=text(language, zh_risk, en_risk),
        deduction=deduction,
        evidence_status=(
            EvidenceStatus.CONFLICT if case == "d" else EvidenceStatus.PARTIALLY_CONFIRMED
        ),
        mitigation=text(
            language,
            "要求客户提供主体、付款和采购参数证明。",
            "Request entity, payment, and purchasing-parameter evidence.",
        ),
        source_ids=["S1"] if case != "c" else [],
    )
    recommendations = _recommendations(case, language)
    signals = {
        "a": [
            PurchaseSignal(
                signal_type=text(language, "明确询价", "Explicit inquiry"),
                detail=text(language, "询问两类耗材价格与交期。", "Asked for price and lead time for two consumable categories."),
                explicit=True,
                evidence_status=EvidenceStatus.CONFIRMED,
                source_ids=["S4"],
            ),
            PurchaseSignal(
                signal_type=text(language, "索样测试", "Sample test"),
                detail=text(language, "要求安排样品测试。", "Requested a sample test."),
                explicit=True,
                evidence_status=EvidenceStatus.CONFIRMED,
                source_ids=["S4"],
            ),
        ],
        "b": [
            PurchaseSignal(
                signal_type=text(language, "普通目录请求", "General catalog request"),
                detail=text(language, "仅索要普通产品目录并保持回复。", "Requested only a general catalog and continued replying."),
                explicit=False,
                evidence_status=EvidenceStatus.PARTIALLY_CONFIRMED,
                source_ids=["S4"],
            )
        ],
        "c": [],
        "d": [],
    }[case]
    priority_actions = {
        "a": ("先确认设备、承印物和测试规格后发送一份定向样品方案。", "Confirm the press, substrate, and test specification, then send one targeted sample plan."),
        "b": ("发送一份两类产品的定向参数表并要求客户补充设备型号。", "Send one targeted two-product parameter sheet and request the press model."),
        "c": ("要求客户提供注册主体、官网和设备信息后再决定是否继续。", "Request the registered entity, website, and equipment details before deciding whether to continue."),
        "d": ("暂停报价并要求付款受益人与注册主体一致的证明。", "Pause quotation and request proof reconciling the beneficiary with the registered entity."),
    }
    action = text(language, *priority_actions[case])
    first_focus = text(
        language,
        "确认设备型号、承印物、现用规格与采购时间。",
        "Confirm equipment model, substrate, current specification, and purchase timing.",
    )
    conditional_product = (
        recommendations[0].recommended_product
        if recommendations
        else text(language, "暂不推荐具体产品", "No specific product recommended")
    )
    conclusions = {
        "a": (
            f"【已确认】客户主体真实，主营纸盒UV胶印，公开信息基本一致。首推"
            f"{'、'.join(item.recommended_product for item in recommendations)}，对应纸盒UV胶印与设备维护场景。"
            f"综合得分97分，最终等级A，值得优先主动开发。最优先行动是{action}最大不确定性为{text(language, zh_risk, en_risk)}。",
            f"[Confirmed] The entity is authentic and operates a folding-carton UV-offset business with broadly consistent public information. "
            f"Priority products are {', '.join(item.recommended_product for item in recommendations)} for carton UV-offset production and press maintenance. "
            f"The score is 97 and the final grade is A, so priority development is warranted. The priority action is: {action} "
            f"The maximum uncertainty is {text(language, zh_risk, en_risk)}.",
        ),
        "b": (
            f"【已确认】客户主体真实，主营纸包装生产，但具体设备仅部分确认。首推"
            f"{'、'.join(item.recommended_product for item in recommendations)}，用于常规胶印纸盒。"
            f"综合得分66分，最终等级B，值得主动开发但暂无明确采购信号。最优先行动是{action}最大不确定性为{text(language, zh_risk, en_risk)}。",
            f"[Confirmed] The entity is authentic and makes paper packaging, while exact equipment is only partly confirmed. "
            f"Priority products are {', '.join(item.recommended_product for item in recommendations)} for conventional offset cartons. "
            f"The score is 66 and the final grade is B; active development is worthwhile but no explicit purchase signal exists. "
            f"The priority action is: {action} The maximum uncertainty is {text(language, zh_risk, en_risk)}.",
        ),
        "c": (
            f"【部分确认】目前只有个人邮箱和电话，客户主体与主营业务无法确认。"
            f"仅可条件性考虑{conditional_product}，实际工艺未知。"
            f"综合得分40分，最终等级C，仅建议低成本核实。最优先行动是{action}最大风险为{text(language, zh_risk, en_risk)}。",
            f"[Partially confirmed] Only a personal email and phone are available; the entity and main business cannot be confirmed. "
            f"{conditional_product} is only a conditional option because the process is unknown. "
            f"The score is 40 and the final grade is C, so only low-cost verification is justified. "
            f"The priority action is: {action} The maximum risk is {text(language, zh_risk, en_risk)}.",
        ),
        "d": (
            f"【信息冲突】客户注册主体可确认，但付款受益人与注册主体严重冲突，主营设备贸易与我司产品匹配较弱。"
            f"目前不建议推荐具体产品。综合得分29分，最终等级D，暂缓开发。"
            f"最优先行动是{action}最大风险为{text(language, zh_risk, en_risk)}。",
            f"[Conflicting information] The registered entity is confirmed, but the payment beneficiary materially conflicts with it; business fit is weak. "
            f"No specific product should be recommended now. The score is 29 and the final grade is D, so development should be deferred. "
            f"The priority action is: {action} The maximum risk is {text(language, zh_risk, en_risk)}.",
        ),
    }
    conclusion = text(language, *conclusions[case])
    questions = [
        FollowUpQuestion(
            priority=1,
            question=text(language, "请提供完整注册主体和注册编号。", "Please provide the full registered entity and registration number."),
            reason=text(language, "核验签约与付款主体。", "Verify contracting and payment entities."),
            subsequent_action=text(language, "核验后更新真实性评分。", "Update authenticity scoring after verification."),
        ),
        FollowUpQuestion(
            priority=2,
            question=text(language, "请提供印刷设备品牌、型号和工艺。", "Please provide the press brand, model, and printing process."),
            reason=text(language, "决定产品和测试参数。", "Determine product and test parameters."),
            subsequent_action=text(language, "生成定向产品方案。", "Prepare a targeted product plan."),
        ),
        FollowUpQuestion(
            priority=3,
            question=text(language, "请说明数量、采购时间和现用品牌。", "Please state quantity, purchase timing, and current brand."),
            reason=text(language, "判断真实采购潜力。", "Assess actual purchase potential."),
            subsequent_action=text(language, "决定报价或低成本跟进。", "Decide whether to quote or use low-cost follow-up."),
        ),
    ]
    return InvestigationReport(
        investigation_date=EXAMPLE_DATE,
        report_language=language,
        mode=mode,
        fictional_notice=FICTIONAL_NOTICE,
        customer=customer,
        verification=verification,
        business_analysis=BusinessAnalysis(
            customer_type=text(
                language,
                "印刷/包装生产商" if case in {"a", "b"} else "无法确认" if case == "c" else "设备贸易商",
                "Printing/packaging manufacturer" if case in {"a", "b"} else "Unable to confirm" if case == "c" else "Equipment trader",
            ),
            main_business=text(
                language,
                "纸盒印刷与包装" if case in {"a", "b"} else "无法确认" if case == "c" else "印刷设备贸易",
                "Folding-carton printing and packaging" if case in {"a", "b"} else "Unable to confirm" if case == "c" else "Printing-equipment trading",
            ),
            business_model=text(language, "B2B直销（虚构示例）", "B2B direct sales (fictional example)"),
            competition_environment=text(language, "未找到可靠公开信息", "No reliable public information was found"),
            evidence_status=statuses[1],
        ),
        production_and_process=ProductionAndProcess(
            printing_processes=(
                [text(language, "UV胶印", "UV offset")]
                if case == "a"
                else [text(language, "胶印", "Offset")]
                if case == "b"
                else []
            ),
            application_scenarios=(
                [text(language, "纸盒包装", "Folding cartons")]
                if case in {"a", "b"}
                else []
            ),
            equipment_models=(
                ["FICTIONAL FP-740 — FICTIONAL TEST MODEL"] if case == "a" else []
            ),
            equipment_note=text(
                language,
                "未找到公开设备型号，需向客户直接确认。" if case != "a" else "设备型号仅用于虚构测试。",
                "No public equipment model was found; confirm directly with the customer." if case != "a" else "The equipment model is fictional test data only.",
            ),
            evidence_status=statuses[2],
        ),
        supplier_and_import_records=SupplierAndImportRecords(
            summary=text(language, "未找到公开可靠记录。", "No reliable public record was found."),
            evidence_status=statuses[3],
        ),
        sales_channels=SalesChannels(
            channels=(
                [text(language, "B2B直销", "B2B direct sales")]
                if case in {"a", "b"}
                else []
            ),
            market_scope=[],
            summary=text(
                language,
                "公开范围有限，需客户确认。",
                "Public evidence is limited; customer confirmation is required.",
            ),
            evidence_status=statuses[4],
        ),
        company_scale=CompanyScale(
            revenue=text(language, "未找到可靠公开信息。", "No reliable public information was found."),
            employee_count=text(language, "未找到可靠公开信息。", "No reliable public information was found."),
            capacity=text(language, "未找到可靠公开信息。", "No reliable public information was found."),
            operating_status=text(
                language,
                "无法确认" if case == "c" else "主体状态已确认，当前经营规模无法确认",
                "Unable to confirm" if case == "c" else "Entity status confirmed; current operating scale cannot be confirmed",
            ),
            summary=text(language, "未找到可靠的规模数据。", "No reliable scale data was found."),
            evidence_status=statuses[5],
        ),
        investigation_items=_investigation_items(language, statuses, case),
        product_recommendations=recommendations,
        purchase_signals=signals,
        follow_up_questions=questions,
        risks=[risk],
        scoring=_score(case, language),
        conclusion=conclusion,
        development_value=text(
            language,
            "值得继续核实" if case in {"a", "b", "c"} else "暂不建议投入",
            "Worth further verification" if case in {"a", "b", "c"} else "Do not invest resources now",
        ),
        first_contact_focus=first_focus,
        evidence_gaps=[
            text(language, "设备型号", "Equipment model"),
            text(language, "现用品牌", "Current brand"),
            text(language, "数量与采购时间", "Quantity and purchase timing"),
        ],
        priority_action=action,
        not_recommended_action=text(
            language,
            "在参数和主体核实前不寄大批样品。",
            "Do not send a large sample batch before entity and parameter verification.",
        ),
        maximum_risk=text(language, zh_risk, en_risk),
        sources=_sources(case, customer, language),
    )


def _dump_model(report: InvestigationReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            report.model_dump(mode="json", exclude_computed_fields=True),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_examples() -> None:
    chinese = make_report("a", ReportLanguage.ZH_CN)
    english = make_report("b", ReportLanguage.EN)
    simplified = make_report("c", ReportLanguage.BILINGUAL)

    chinese_dir = ROOT / "examples" / "chinese-user-overseas-customer"
    english_dir = ROOT / "examples" / "international-user-chinese-customer"
    batch_dir = ROOT / "examples" / "batch-investigation"
    for directory in (chinese_dir, english_dir, batch_dir):
        directory.mkdir(parents=True, exist_ok=True)

    chinese_json = chinese_dir / "FICTIONAL_Aurora_Printworks_investigation.json"
    _dump_model(chinese, chinese_json)
    generate_docx(chinese, chinese_dir / "FICTIONAL_Aurora_Printworks_客户背景调查报告.docx")
    generate_xlsx(chinese, chinese_dir / "FICTIONAL_Aurora_Printworks_客户背景调查数据.xlsx")

    english_json = english_dir / "FICTIONAL_Horizon_Packaging_investigation.json"
    _dump_model(english, english_json)
    generate_docx(english, english_dir / "FICTIONAL_Horizon_Packaging_Customer_Background_Report.docx")
    generate_xlsx(english, english_dir / "FICTIONAL_Horizon_Packaging_Customer_Investigation_Data.xlsx")

    reports = [chinese, english, simplified]
    ranking = rank_reports(reports)
    (batch_dir / "batch-investigation.json").write_text(
        json.dumps(
            {
                "fictional_notice": FICTIONAL_NOTICE,
                "reports": [
                    report.model_dump(mode="json", exclude_computed_fields=True)
                    for report in reports
                ],
                "ranking": [entry.model_dump(mode="json") for entry in ranking],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    generate_xlsx(
        chinese,
        batch_dir / "FICTIONAL_Batch_Development_Ranking.xlsx",
        ranking=ranking,
    )

    templates = SKILL / "templates"
    templates.mkdir(parents=True, exist_ok=True)
    generate_docx(chinese, templates / "report-template-zh.docx")
    generate_docx(english, templates / "report-template-en.docx")
    generate_xlsx(chinese, templates / "investigation-template.xlsx")


if __name__ == "__main__":
    build_examples()
