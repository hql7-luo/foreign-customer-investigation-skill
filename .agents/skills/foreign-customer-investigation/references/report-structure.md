# Output and Report Structure

## Contents

- One-data-object rule
- Word
- Excel
- JSON
- Cross-output consistency
- File and encoding rules

## One-data-object rule

Populate one validated `InvestigationReport` object. Generate all outputs with:

```text
InvestigationReport
├── DOCX
├── XLSX
└── JSON
```

Never author conclusions separately. The customer name, investigation date, score, grade, recommended products, maximum risk, and priority action must match exactly.

## Word — full mode

Filename:

```text
Company_Name_客户背景调查报告.docx
```

Use an English name or transliteration in the filename when the legal name contains unsafe symbols. Preserve the full legal name in the title.

### 1. Conclusion

Use 3-5 sentences and include:

- Authenticity
- Main business type
- First-choice product(s)
- Application scenario
- Final score
- One final grade
- Whether active development is worthwhile
- One priority action
- Maximum risk or uncertainty

### 2. Nine-part investigation table

Use:

| No. | Investigation item | Core finding |
|---:|---|---|

Keep all nine items and evidence labels. Ordinary findings should stay concise.

### 3. Sales action card

Use:

| Item | Recommendation |
|---|---|
| Final grade | A/B/C/D and total score |
| Priority products | One to three categories |
| First-contact focus | Most important point to confirm |
| Current evidence gaps | Quantity, equipment, brand, timing, etc. |
| Priority action | Exactly one |
| Action not recommended | Resource not worth committing yet |

### 4. Core sources

List three to five complete URLs, one per line, without a table. Do not include search result URLs.

### Layout

- Normally two pages or fewer
- Center title; show investigation date below it
- Deep-blue bold first-level headings
- Light-blue table headers
- Clear, compact business tables
- Avoid long paragraphs and large blank areas
- No logo, screenshot, or AI-generated image by default
- Exclude search process, internal reasoning, scoring drafts, and self-check lists

Support Chinese, English, and requested bilingual versions.

## Word — simplified mode

Output only:

1. Conclusion
2. Development value
3. Confirmed information
4. Questions to verify directly
5. Core sources

Keep the score and grade inside the conclusion so cross-output consistency remains auditable.

## Excel

Create at least:

1. `Customer Overview`
   - Company, brand, country, contact, title, website, email, phone, main business, grade, score, products, action, risk, date
2. `Investigation`
   - Number, item, finding, evidence state, sources, confirmation needed
3. `Scoring Details`
   - Dimension, item, maximum, actual score, rationale, evidence state
   - Include formula total, risk deductions, score validation, grade formula, and grade validation
4. `Evidence and Sources`
   - ID, title, URL, source type, access date, supported conclusion, credibility, information year
5. `Follow-up Questions`
   - Priority, question, reason, customer answer, subsequent action
6. `Development Ranking`
   - Rank, company, grade, score, products, purchase signal, risk, action

Freeze headers, enable filters, use readable widths and wrapping, apply conditional formatting for grades, hide gridlines where structure is explicit, and do not use macros.

For batch reports, ranking numbers must be unique even when scores tie.

## JSON

Keep field names in English and UTF-8 encoding:

```json
{
  "investigation_date": "YYYY-MM-DD",
  "report_language": "zh-CN",
  "mode": "full",
  "customer": {},
  "verification": {},
  "business_analysis": {},
  "production_and_process": {},
  "supplier_and_import_records": {},
  "sales_channels": {},
  "company_scale": {},
  "investigation_items": [],
  "product_recommendations": [],
  "purchase_signals": [],
  "follow_up_questions": [],
  "risks": [],
  "scoring": {},
  "priority_action": "",
  "maximum_risk": "",
  "sources": []
}
```

Stable enum codes remain English for machine processing; narrative values follow the report language.

## Cross-output consistency

Run `scripts/validate_report.py` after generation. It must check:

- One legal grade and a valid score
- Grade restrictions
- Up to three recommendations
- One priority action
- Three to five core sources
- Simplified-mode trigger
- No placeholders or internal-process content
- Matching critical conclusions in Word, Excel, and JSON
- Unique batch ranks
- UTF-8/non-Latin preservation
- Phone country prefix preservation

## File and encoding rules

- Use UTF-8 JSON and source files.
- Use Unicode-capable Word/Excel fonts.
- Preserve Chinese, Russian, Arabic, and European-language text.
- Use cross-platform safe filenames and `pathlib`.
- Verify DOCX and XLSX open with Microsoft Office and LibreOffice when available.
