# Source Reliability and Search

## Contents

- Source hierarchy
- Allowed search
- Query construction
- Source-record schema
- Sanctions and compliance

## Source hierarchy

Use the highest available source tier and cross-verify material claims:

1. Government, official business/tax/court registries, official sanctions and regulator lists
2. Company website, official social account, official newsroom
3. Exhibition organizer, recruitment site, map platform, industry association
4. Industry media, distributor page, B2B marketplace
5. Registry aggregator
6. Commercial directory, forum, individual post

Low-tier sources may supply leads but must not independently prove:

- Legal entity
- Revenue or financial strength
- Supplier
- Customer
- Cooperation brand
- Import/customs record
- Purchase record

Never describe a commercial directory as an official registry.

## Allowed search

Use public pages that do not require authentication. Do not:

- Bypass CAPTCHA, paywall, robot protection, or access control
- Use leaked, stolen, or private data
- Use private browser history, cookies, credentials, or customer files beyond the user's supplied scope
- Claim access to paid customs databases
- Collect unrelated personal data

If an official system is inaccessible, record the access limitation and use secondary sources only as partial evidence.

## Query construction

Combine:

- Formal company name
- Brand/trading name
- English name
- Local-language name
- Contact name
- Email domain
- Phone
- Address
- Website domain
- Registration and local tax identifier
- Product
- Equipment brand
- Exhibition

Search local language plus English; add Chinese only when it helps the user's investigation. For Russian and Russian-language markets, useful query terms include:

```text
official website
ИНН
ОГРН
ЕГРЮЛ
отзывы
клиенты
поставщики
производство
печать
полиграфия
упаковка
краска
УФ печать
LED UV
оборудование
импорт
вакансии
дистрибьютор
дилер
```

Prefer exact-name queries first. Use phone, email domain, address, and registration number to disambiguate common names.

## Source-record schema

Record for every retained source:

| Field | Requirement |
|---|---|
| Source ID | Unique within report |
| Page title | Exact or faithful page title |
| Full URL | Direct page URL, not search result |
| Source type | Registry, company, map, association, media, directory, etc. |
| Access date | `YYYY-MM-DD` |
| Supported conclusion | Specific fact or inference supported |
| Credibility | High, medium, or low |
| Information year | Publication/record year when known |
| Core source | Select 3-5 per report |

Do not list duplicate URLs or irrelevant homepages when a more specific supporting page exists.

## Sanctions and compliance

Check current official sources applicable to the transaction path, such as:

- United Nations Security Council sanctions
- Relevant national or regional consolidated lists
- Export-control or denied-party lists that apply to the seller, goods, intermediaries, banks, or route
- Official court/registry notices relevant to entity status

Search the exact legal name, local-language name, known aliases, registration number, address, and controlling parties only when publicly and lawfully available.

A country-level risk context is not an entity listing. Report:

1. The exact matched name and identifier.
2. The official list and current record.
3. Whether the match is confirmed, partial, or conflicting.
4. The transaction impact requiring specialist review.

Never state that an entity is sanctioned based only on nationality, language, or location.
