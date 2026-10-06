# Foreign Customer Investigation Skill

[![Validation](https://github.com/hql7-luo/foreign-customer-investigation-skill/actions/workflows/validation.yml/badge.svg)](https://github.com/hql7-luo/foreign-customer-investigation-skill/actions/workflows/validation.yml)

[中文说明](README.zh-CN.md)

`foreign-customer-investigation` is a reusable Agent Skill for evidence-based B2B customer investigation, printing-industry product-fit analysis, purchase-potential scoring, and development prioritization.

It supports investigations in every direction:

- Chinese suppliers investigating overseas customers
- Overseas suppliers investigating Chinese customers
- Chinese companies investigating Chinese customers
- International companies investigating customers in third countries
- Manufacturers, distributors, equipment vendors, printers, packaging converters, and end users

The conclusion is based on the investigated customer and transaction evidence, never on the investigator's nationality.

> This tool supports commercial research. It does not replace legal advice, formal credit checks, sanctions screening by qualified professionals, or customer verification required by your organization.

## Features

- Verifies company entity, website, contact, phone, email, address, and information consistency
- Determines customer type, main business, business model, printing process, equipment clues, and applications
- Maps customer evidence to one to three printing consumable or maintenance product categories
- Identifies explicit inquiry, sample, test, quotation, quantity, timing, supplier-problem, reply, and next-step signals
- Checks public entity, payment, logistics, sanctions, export-control, and transaction-path risks
- Calculates a traceable `0..100` score from line items
- Produces exactly one `A`, `B`, `C`, or `D` development grade
- Selects exactly one priority action
- Produces consistent DOCX, XLSX, and UTF-8 JSON from one Pydantic model
- Supports single-customer and no-tie batch rankings
- Supports Chinese, English, requested bilingual reports, and non-Latin input
- Enforces simplified mode when evidence is inadequate
- Includes automated validation for grade rules, output consistency, placeholders, source count, ranking, and Unicode

## When to use

Typical triggers:

```text
调查这个国外客户
帮我查一下这个客户背景
判断这个客户值不值得开发
根据名片调查客户
分析客户采购潜力
给客户做背景调查报告
给这些客户排开发优先级
调查该客户适合推荐什么印刷耗材

Investigate this customer
Conduct customer due diligence
Assess this buyer's purchase potential
Generate a customer background report
```

The full workflow should not trigger for:

- Translation-only requests
- Sales-email drafting only
- A single website lookup
- Company-name explanation only
- Generic product recommendations without an investigation request

## Product scope

The matching guide covers:

- Printing consumables
- Offset ink
- UV ink
- LED UV products
- Printing plates
- Blankets
- Fountain solution
- Cleaning agents
- Printing-equipment spare parts
- Cooling systems and related parts
- Other printing, packaging, and maintenance products

Recommendations must follow:

```text
verified customer product or equipment
→ printing process
→ consumable or maintenance need
→ 1-3 specific product categories
```

The Skill never lists the entire catalog by default.

## Installation

Requirements:

- Python 3.11+
- `python-docx`
- `openpyxl`
- `pydantic`
- `pytest`

```bash
git clone https://github.com/hql7-luo/foreign-customer-investigation-skill.git
cd foreign-customer-investigation-skill
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements-lock.txt
```

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements-lock.txt
```

Python 3.11 and 3.12 are validated in CI. `requirements-lock.txt` pins the tested dependency snapshot with hashes; `requirements.txt` records the supported ranges. Pydantic 2.12+ is required for computed-field serialization.

The repository already stores the Skill at:

```text
.agents/skills/foreign-customer-investigation/
```

Use it from this repository or copy that folder into another Agent Skill search path supported by your environment.

## Directory structure

```text
foreign-customer-investigation-skill/
├── .agents/
│   └── skills/
│       └── foreign-customer-investigation/
│           ├── SKILL.md
│           ├── agents/
│           │   └── openai.yaml
│           ├── references/
│           │   ├── investigation-rules.md
│           │   ├── scoring-rules.md
│           │   ├── evidence-rules.md
│           │   ├── source-reliability.md
│           │   ├── report-structure.md
│           │   ├── simplified-mode.md
│           │   ├── country-adaptation.md
│           │   └── product-matching-guide.md
│           ├── templates/
│           │   ├── customer-input-template-zh.md
│           │   ├── customer-input-template-en.md
│           │   ├── report-template-zh.docx
│           │   ├── report-template-en.docx
│           │   └── investigation-template.xlsx
│           └── scripts/
│               ├── models.py
│               ├── generate_docx.py
│               ├── generate_xlsx.py
│               ├── generate_json.py
│               ├── validate_report.py
│               └── file_utils.py
├── examples/
│   ├── chinese-user-overseas-customer/
│   ├── international-user-chinese-customer/
│   ├── batch-investigation/
│   └── build_examples.py
├── tests/
├── requirements.txt
├── README.md
├── README.zh-CN.md
├── LICENSE
└── .gitignore
```

Detailed rules live in `references/`; `SKILL.md` stays focused on triggering, workflow, non-fabrication, outputs, and reference routing.

## Input

Fields may be missing. Every missing decision-relevant field becomes an evidence gap.

### Chinese input example

```text
公司名：FICTIONAL Aurora Printworks Sp. z o.o.
品牌名：FICTIONAL Aurora
联系人：Maya Example
职位：Purchasing Manager
电话：+999 000 000 001
邮箱：maya.example@aurora-print.example
官网：https://aurora-print.example
地址：1 Fictional Avenue, Example City, Poland
国家/地区：Poland
手写备注：FICTIONAL EXAMPLE — NOT A REAL COMPANY
客户提出的需求：询问UV油墨与橡皮布，并要求测试样品
沟通记录：已回复并确认下一步测试参数
其他线索：纸盒UV胶印
```

Chinese input defaults to a Chinese report.

### English input example

```text
Company legal name: 虚构远景包装技术有限公司
Trading name / Brand: FICTIONAL Horizon
Contact: Alex Example
Job title: Operations Manager
Phone: +999 000 000 002
Email: alex.example@fictional-horizon.example
Website: https://fictional-horizon.example
Address: 中国示例省虚构市示例路2号（虚构地址）
Country / Region: China
Notes: FICTIONAL EXAMPLE — NOT A REAL COMPANY
Customer requirements: Requested only a general product catalog
Communication history: Replies continue; no quotation or sample request
Other clues: Paper-carton production
```

English input defaults to an English report. Ask explicitly for `bilingual` when required.

Original-language names and addresses are preserved next to transliteration/translation. A leading `+` in phone numbers is not removed.

## Usage

### Agent invocation

```text
Use $foreign-customer-investigation to investigate this customer.
Generate Chinese Word, Excel, and JSON outputs.
```

```text
Use $foreign-customer-investigation to conduct customer due diligence.
Preserve the Chinese legal name and generate an English report.
```

The Agent should research public, non-login sources, populate one validated `InvestigationReport`, and run the three generators.

### Generate outputs from validated JSON

```bash
SKILL=.agents/skills/foreign-customer-investigation
python "$SKILL/scripts/generate_json.py" investigation.json --output-dir outputs
python "$SKILL/scripts/generate_docx.py" investigation.json --output-dir outputs
python "$SKILL/scripts/generate_xlsx.py" investigation.json --output-dir outputs
```

### Validate cross-output consistency

```bash
python "$SKILL/scripts/validate_report.py" investigation.json \
  --docx outputs/Company_Name_Customer_Background_Report.docx \
  --xlsx outputs/Company_Name_Customer_Investigation_Data.xlsx \
  --generated-json outputs/Company_Name_investigation.json
```

### Rebuild fictional examples

```bash
python examples/build_examples.py
```

Every example is labeled:

```text
FICTIONAL EXAMPLE — NOT A REAL COMPANY
```

No real company contact, email, phone, address, communication, quotation, or customer record is used.

## Single-customer example

See:

- `examples/chinese-user-overseas-customer/`
- `examples/international-user-chinese-customer/`

Each directory contains matching Word, Excel, and JSON conclusions.

## Batch investigation

Use the same model for each customer and call `rank_reports()`:

```python
from models import rank_reports

ranking = rank_reports(reports)
```

Ranking order:

1. Purchase signal
2. Product/application fit
3. Contact execution and reply
4. Repeat or volume potential
5. Information completeness
6. Risk
7. Total score

A deterministic name/input-order tiebreaker prevents tied rank numbers. See `examples/batch-investigation/`.

## China-customer investigation

For a Chinese customer, preserve the Chinese legal name and check the country-appropriate official registry and identifier, such as the Unified Social Credit Code when applicable. Do not replace it with VAT, EIN, INN, or OGRN.

The English fictional example in `examples/international-user-chinese-customer/` demonstrates an overseas user investigating a Chinese packaging producer.

## Overseas-customer investigation

Select registry, tax identifiers, language, map, social/B2B platforms, sanctions sources, phone/address format, currency, and timezone by country. The Chinese fictional example in `examples/chinese-user-overseas-customer/` demonstrates a Chinese user investigating a Polish customer.

Official systems can be inaccessible, jurisdiction-specific, or protected by CAPTCHA. The Skill reports those limitations and does not disguise a commercial directory as official confirmation.

## Outputs

### Word

- Full mode: conclusion, nine-part summary, sales action card, and 3-5 core URLs
- Simplified mode: conclusion, development value, confirmed information, direct-verification questions, and core URLs
- Centered title, investigation date, deep-blue headings, light-blue table headers
- Compact business layout, normally two pages or fewer
- Chinese, English, and requested bilingual reports

### Excel

Six worksheets:

1. Customer Overview
2. Investigation
3. Scoring Details
4. Evidence and Sources
5. Follow-up Questions
6. Development Ranking

The workbook includes visible score formulas, risk deductions, total/grade validation formulas, filters, frozen headers, wrapping, widths, and grade conditional formatting. It uses no macros.

### JSON

- English field names
- UTF-8 narrative content
- ISO date and country conventions where available
- Machine-stable enum values
- Same customer name, date, score, grade, products, risk, and action as Word/Excel

## Evidence states

| State | Meaning |
|---|---|
| Confirmed | Official evidence, cross-verification, or at least two independent reliable sources |
| Partially confirmed | One company source, aggregator, customer/card/exhibition clue, or old information |
| Inferred | Reasoned from process, consumable behavior, maintenance, seasonality, or business model; basis stated |
| Conflicting information | Material sources disagree; every relevant version is retained |
| Not found | Reliable public evidence was not located; this never means “does not exist” |

## Source reliability

Priority:

1. Official government, registry, tax, court, sanctions, and regulator sources
2. Company website and official channels
3. Exhibition, recruitment, map, and industry association
4. Industry media, distributor, and B2B marketplace
5. Registry aggregator
6. Directory, forum, or personal post

Low-reliability sources cannot independently prove entity identity, revenue, suppliers, customers, cooperation brands, imports, customs records, or purchases.

## Scoring

| Dimension | Maximum |
|---|---:|
| Authenticity | 20 |
| Business fit | 25 |
| Purchase signal | 25 |
| Purchase potential | 15 |
| Contact execution | 15 |
| Risk deduction | 0 to -20 |

Total is clamped to `0..100`. Every dimension is built from auditable line items.

## Grades

| Grade | Typical score | Meaning |
|---|---:|---|
| A | 80-100 | Authentic, high fit, explicit purchase signal, no material risk |
| B | 60-79 | Worth active development; key purchase details remain unclear |
| C | 40-59 | Low-cost follow-up; weak signals or incomplete public evidence |
| D | Below 40 or severe verified risk | Defer |

Mandatory restrictions:

- No explicit purchase signal → maximum B
- No website plus unconfirmed entity → maximum C
- Authenticity doubtful → never A
- Company size or contact title alone → never A
- Simplified mode → normally C or D
- Only `A`, `B`, `C`, or `D`; no modifiers

## Simplified mode

Simplified mode activates when any applies:

- Five or more investigation areas lack reliable evidence
- No website
- Entity cannot be confirmed
- Name/email/phone/address cannot be cross-verified
- Company name is too generic
- Only a personal email/social account exists
- Normal scoring is not supportable

Development value must be one of:

- Worth further verification
- Low-cost monitoring
- Do not invest resources now

## Non-fabrication

Never invent:

- Revenue
- Employees
- Capacity
- Customers or suppliers
- Cooperation brands
- Imports or customs data
- Equipment models
- Purchase quantity or cycle

Use “No reliable public information was found,” “No reliable public record was found,” or “Unable to confirm.” Do not convert “not found” into “does not exist.”

## Privacy and data compliance

- Use public, lawful, non-login sources
- Do not bypass CAPTCHA, paywalls, access controls, or privacy protections
- Do not use leaked or private datasets
- Do not commit real customer identity, personal email, phone, address, communications, quotations, credentials, cookies, browser data, or API keys
- Review sanctions and export-control risks using current official sources and exact entity matching
- Do not assign sanctions risk based only on country

The `.gitignore` excludes common secret and private-customer paths. A repository scan is still required before every public push.

## Known limitations

- Public data can be incomplete, stale, inconsistent, region-blocked, or unavailable
- The Skill cannot automatically access every national registry
- It does not access paid customs databases
- It cannot guarantee that an online identity or contact is genuine
- It does not provide an absolute-accuracy guarantee
- It does not replace legal, credit, sanctions, export-control, tax, or compliance review
- Word and Excel rendering can vary slightly by installed fonts and office software

## Testing

```bash
pytest -q
```

Research strings are written as literal Excel text; only the generator's scoring and grade checks become formulas. The privacy checks audit publication files and exclude ignored local environments and report outputs.

Tests cover A/B/C/D cases, simplified-mode triggers, grade caps, score bounds, risk deductions, DOCX/XLSX/JSON generation, formulas, cross-output consistency, no-tie rankings, recommendation limits, Chinese/English/mixed input, China/overseas cases, and non-Latin characters.

## License

[MIT License](LICENSE)
