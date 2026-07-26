# Country Adaptation

## Contents

- Adaptation checklist
- Example country/region routes
- Identifiers and formats
- High-risk markets

## Adaptation checklist

Determine the customer's country from reliable evidence, then adapt:

- Search language and transliteration
- Official business registry
- Tax/registration identifiers
- Map/address source
- Common professional/social platform
- Common B2B marketplace
- Sanctions and export-control sources applicable to the transaction
- Address and phone format
- Date, currency, and timezone

Do not infer the report conclusion from the investigator's country. Do not assume every customer uses Chinese unified social credit code, VAT, EIN, INN, OGRN, USD, or FOB.

If country cannot be confirmed, state the gap and avoid country-specific identifier claims.

## Example routes

| Market | Typical official checks | Identifier examples | Notes |
|---|---|---|---|
| China | National Enterprise Credit Information Publicity System and relevant official regulator/tax sources | Unified Social Credit Code | Preserve Chinese legal name; distinguish brand from entity |
| United States | Secretary of State for the relevant state; SEC only where applicable | State file number, EIN when lawfully/publicly available | State registration is decentralized |
| European Union | National business registry; VIES for VAT validation when applicable | National company number, VAT ID | VIES does not replace national entity verification |
| United Kingdom | Companies House and relevant official regulators | Company number, VAT when applicable | Use filing status and filing dates |
| Russia | Federal Tax Service/ЕГРЮЛ and official sources | ИНН, ОГРН | Search Cyrillic legal name and identifiers |
| India | Ministry of Corporate Affairs; GST and DGFT systems where relevant | CIN, GSTIN, IEC | Match legal name and state/address |
| Middle East | Country-specific commercial registry, tax authority, chamber, and free-zone authority | Varies by country/free zone | Do not treat the region as one registry system |

These are routes, not guarantees of access. Official systems may impose regional access, CAPTCHA, or data limits. Record the limitation; never bypass it or substitute a low-trust directory as official proof.

## Identifiers and formats

- Country: ISO 3166 alpha-2 when possible
- Currency: ISO 4217
- Language: ISO 639
- Date: `YYYY-MM-DD`
- Phone: retain `+` and country code; do not normalize away digits
- Timezone: use a named local timezone when relevant
- Address: preserve original order and script; add transliteration/translation separately

Tax identifiers are country- and entity-type-specific. A missing VAT number does not invalidate a non-VAT jurisdiction or exempt business. A missing EIN is not a valid finding outside the United States.

## High-risk markets

Country context may affect:

- Applicable sanctions lists
- Export licensing
- Banking and payment routing
- Insurance
- Carrier availability
- Customs documentation
- Transshipment risk

Treat these as transaction-path questions. Do not automatically identify every entity in a higher-risk jurisdiction as sanctioned, fraudulent, or unpayable. Match exact entities against current official lists and escalate material matches for specialist legal/compliance review.
