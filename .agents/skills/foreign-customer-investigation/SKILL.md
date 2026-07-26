---
name: foreign-customer-investigation
description: Investigate and prioritize B2B customers worldwide using public evidence, country-adapted entity verification, printing-process and product-fit analysis, purchase-signal scoring, compliance risk checks, and consistent Word, Excel, and JSON outputs. Use for requests such as “调查这个客户”, “判断这个客户值不值得开发”, “根据名片调查客户”, “给这些客户排开发优先级”, “Investigate this customer”, “Conduct customer due diligence”, or “Assess this buyer’s purchase potential”. Do not invoke for translation-only, sales-copy-only, single-website lookup, company-name explanation, or generic product recommendation requests that do not ask for investigation.
---

# Foreign Customer Investigation

## Purpose

Verify a customer and contact, assess business and printing-process fit, identify purchase signals and risks, calculate one 0-100 score and one A/B/C/D grade, select one priority action, and generate consistent Word, Excel, and JSON deliverables. Apply the conclusions to the investigated customer itself; never infer risk, demand, or grade from the investigator's nationality.

Support investigations in any direction, including Chinese suppliers investigating overseas buyers, overseas suppliers investigating Chinese buyers, domestic investigations, cross-border third-country investigations, and relationships among manufacturers, distributors, equipment vendors, printers, packaging converters, and end users.

## Trigger boundary

Run the full workflow when the user requests background investigation, customer due diligence, purchase-potential assessment, product-fit research, a background report, or multi-customer prioritization.

Do not run the full workflow when the user only asks to translate a message, draft outreach, open one website, explain a company name, or recommend a product without investigation. Complete only the requested narrow task.

## Standard workflow

1. Parse the supplied card, company data, communication, requirements, and notes. Preserve original-language names, transliterations, and translations. Treat user-supplied material as clues until verified.
2. Detect report language: Chinese input → `zh-CN`; English input → `en`; use `zh-CN+en` only when requested. Keep JSON field names in English.
3. Identify the country and load [country-adaptation.md](references/country-adaptation.md). Choose appropriate local-language queries, official registries, tax identifiers, maps, social platforms, sanctions sources, formats, currency, and timezone.
4. Research public, non-login sources. Do not bypass paywalls, CAPTCHAs, access controls, or privacy safeguards. Load [source-reliability.md](references/source-reliability.md) and [evidence-rules.md](references/evidence-rules.md).
5. Complete the nine investigation areas and supply-chain checks described in [investigation-rules.md](references/investigation-rules.md). Retain conflicts instead of resolving them without evidence.
6. Map only verified or explicitly inferred customer products/equipment to process → need → one to three product categories. Load [product-matching-guide.md](references/product-matching-guide.md).
7. Score every line item, apply risk deductions and grade caps, and select exactly one priority action. Load [scoring-rules.md](references/scoring-rules.md).
8. Enable simplified mode whenever a trigger in [simplified-mode.md](references/simplified-mode.md) applies.
9. Populate one `InvestigationReport` object from `scripts/models.py`. Generate every output from that object; never author separate conclusions.
10. Generate Word, Excel, and JSON with the scripts in `scripts/`, then run `scripts/validate_report.py`. For batch work, use `rank_reports()` and preserve unique sequential ranks.
11. Follow [report-structure.md](references/report-structure.md). Render Word and Excel for visual QA when the environment supports it; inspect for clipping, broken tables, formula errors, and non-Latin glyph corruption.

## Non-fabrication rules

Never invent revenue, employee count, capacity, customer or supplier names, cooperation brands, import or customs records, equipment models, purchase quantity, or purchase cycle.

Use the report language's equivalent of:

- “未找到可靠公开信息 / No reliable public information was found.”
- “未找到公开可靠记录 / No reliable public record was found.”
- “无法确认 / Unable to confirm.”

State “not found,” never “does not exist.” Mark inferences and their basis. A company website proves only what the company publishes; it does not independently prove current capacity, customers, suppliers, purchases, or operating scale.

## Output contract

- Keep one investigation date, customer name, total score, final grade, recommended products, maximum risk, and priority action identical across Word, Excel, and JSON.
- Recommend one to three product categories. Never list the entire product catalog.
- Retain three to five core sources as complete page URLs; exclude search-result pages.
- Use exactly one grade: `A`, `B`, `C`, or `D`. Do not use modifiers.
- Use exactly one priority action.
- Exclude search logs, internal reasoning, scoring drafts, and self-check lists from deliverables.
- Keep real customer data, credentials, cookies, quotations, communications, and private files out of public repositories.

## Script usage

Run scripts with Python 3.11+ and dependencies from `requirements.txt`:

```bash
python scripts/generate_json.py investigation.json --output-dir outputs
python scripts/generate_docx.py investigation.json --output-dir outputs
python scripts/generate_xlsx.py investigation.json --output-dir outputs
python scripts/validate_report.py investigation.json \
  --docx outputs/report.docx \
  --xlsx outputs/data.xlsx \
  --generated-json outputs/investigation.json
```

Use templates only as layout starting points. Replace template content with validated report data before delivery.
