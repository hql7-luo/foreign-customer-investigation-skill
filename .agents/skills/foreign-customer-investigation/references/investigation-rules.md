# Investigation Rules

## Contents

- Input normalization
- Nine-part investigation
- Research workflow
- Supply-chain and purchase analysis
- Internationalization
- Batch investigations

## Input normalization

Accept missing fields but record the evidence gap. Parse either language:

| Chinese | English |
|---|---|
| 公司名 | Company legal name |
| 品牌名 | Trading name / Brand |
| 联系人 | Contact |
| 职位 | Job title |
| 电话 | Phone |
| 邮箱 | Email |
| 官网 | Website |
| 地址 | Address |
| 国家/地区 | Country / Region |
| 手写备注 | Notes |
| 客户提出的需求 | Customer requirements |
| 沟通记录 | Communication history |
| 其他线索 | Other clues |

Preserve:

1. Original-language legal name and address.
2. English name or transliteration.
3. Chinese translation when useful.
4. Country prefix in phone numbers, including the leading `+`.

Do not translate away Russian, Arabic, Spanish, Chinese, or other original text. Treat business cards, handwritten notes, emails, and oral statements as customer-provided evidence, not verified public fact.

## Nine-part investigation

Complete all nine items in full mode:

1. **Company entity and contact authenticity**
   - Legal and trading names
   - Registration status and locally appropriate identifier
   - Website ownership and email-domain alignment
   - Phone, address, and map record
   - Contact identity and role
   - Cross-source consistency and conflicts
2. **Main business, customer type, and competition**
   - Manufacturer, distributor, printer, packaging converter, equipment vendor, service provider, or end user
   - Main products/services and business model
   - Direct and indirect competitive context supported by public evidence
3. **Production equipment, printing processes, and applications**
   - Offset, flexographic, gravure, screen, digital, UV, LED UV, labels, folding cartons, flexible packaging, metal printing, finishing, or maintenance
   - Publicly supported equipment information
   - When absent, write: “未找到公开设备型号，需向客户直接确认 / No public equipment model was found; confirm directly with the customer.”
4. **Current suppliers, cooperation brands, and import records**
   - Public brands, distributorships, current supplier clues, supplier countries, imports, customs records, or supplier changes
   - Never claim access to paid customs databases
   - When absent, write: “未找到公开可靠记录 / No reliable public record was found.”
5. **Sales channels and market scope**
   - Direct sales, distribution, ecommerce, B2B, retail, contract production, or export channels
   - Countries or regions actually supported by evidence
6. **Company scale, capacity, and operating status**
   - Use only reliable, dated public information
   - Never infer revenue, employees, capacity, or financial strength from website appearance
7. **Product fit and recommendations**
   - Use the mapping in `product-matching-guide.md`
   - Recommend no more than three categories
8. **Purchase signals, frequency, and follow-up timing**
   - Separate observed signals from inferred recurring demand
   - Do not invent quantities, budgets, schedules, or cycles
9. **Purchase pain points, risks, and entry plan**
   - Identify the highest uncertainty or risk
   - Give one practical entry approach and one priority action

Keep ordinary Word table findings concise, normally no more than 60 Chinese characters or a similar English length. Items 7-9 may be slightly longer when necessary.

## Research workflow

1. Build query variants from legal name, brand, English name, local-language name, contact, email domain, phone, address, website domain, registration/tax ID, products, equipment brands, and exhibitions.
2. Verify entity identity before treating other pages as belonging to the customer.
3. Search official registry, tax, court, sanctions, and regulator sources appropriate to the country.
4. Cross-check the company website with registry, map, association, exhibition, or other reliable sources.
5. Investigate business/process information.
6. Investigate supply-chain and public import claims.
7. Check current sanctions and export-control lists for the exact entity and known aliases. Do not assign sanctions risk based only on country.
8. Retain every material conflict.
9. Record page title, full URL, source type, access date, supported conclusion, credibility, and information year.

Do not log in, bypass CAPTCHA, scrape restricted personal data, or use leaked/non-public datasets.

## Supply-chain and purchase analysis

Investigate public evidence for:

- Cooperation or represented brands
- Existing brands and supplier-country clues
- Import or customs records
- Distribution relationships
- Supplier changes
- Logistics, sanctions, or supply interruption that may create a substitution window

Low-reliability directories must not independently prove a supplier, customer, brand, import, or purchase record. If no reliable record is found, say so explicitly without converting absence of evidence into evidence of absence.

Recognize these purchase signals:

- Explicit product, price, quantity, specification, or delivery inquiry
- Sample request
- Test request or test plan
- Quotation request
- Equipment model or technical parameter supplied
- Purchase timing supplied
- Current supplier problem disclosed
- Continued replies
- Next step confirmed

A request for a general catalog without a specific requirement normally earns no more than 5 purchase-signal points.

## Internationalization

- Chinese input defaults to a Chinese report.
- English input defaults to an English report.
- Generate bilingual output only when explicitly requested.
- Keep JSON keys in English and narrative values in the report language.
- Use ISO 3166 country codes, ISO 4217 currency codes, ISO 639 language codes, and `YYYY-MM-DD`.
- Use the customer's country to choose formats; never default every case to USD, VAT, EIN, INN, OGRN, Chinese credit code, or FOB.

## Batch investigations

Create one validated report object per customer, then rank by:

1. Purchase signal
2. Product and application fit
3. Contact decision relevance and reply
4. Repeat or volume potential
5. Information completeness
6. Risk
7. Total score

Apply a deterministic final name/input-order tiebreaker and assign unique ranks `1..N`. Do not use tied rank numbers.
