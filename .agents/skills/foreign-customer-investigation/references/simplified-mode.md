# Simplified Mode

## Trigger

Enable simplified mode when any condition is true:

- Five or more of the nine investigation areas lack reliable public information.
- No website exists in the supplied or researched evidence.
- The legal entity cannot be confirmed.
- Company name, email, phone, and address cannot be cross-verified.
- The company name is too generic to disambiguate.
- Only a personal email or social account is available.
- Information is insufficient for normal scoring.

The model function `should_use_simplified_mode()` enforces these triggers.

## Required structure

Output only:

1. Conclusion
2. Development value judgment
3. Confirmed information list
4. Questions the salesperson should verify directly
5. Core sources

Do not pad the report with nine long “not found” paragraphs.

## Development value

Choose one:

- `值得继续核实 / Worth further verification`
- `低成本观察 / Low-cost monitoring`
- `暂不建议投入 / Do not invest resources now`

## Grade

Severely incomplete information is normally C or D:

- C when limited evidence suggests plausible fit and low-cost verification is sensible.
- D when the entity cannot be meaningfully identified, the business is irrelevant, contact data is abnormal, or a severe confirmed risk exists.

Do not use simplified mode to conceal unsupported assumptions. Apply the normal scoring table using only available evidence, then apply the simplified-mode grade cap.

## Direct verification questions

Prioritize questions that would change the commercial decision, such as:

- Exact registered legal name and registration/tax identifier
- Official website and business email
- Factory/office address and landline
- Contact role and purchasing responsibility
- Printing process and equipment brand/model
- Current product specification and application
- Quantity, test plan, purchase timing, and budget
- Current supplier/brand and reason for considering alternatives
- Delivery country, consignee, payment entity, bank, and trade route

Ask only the smallest set needed to resolve the highest-value evidence gaps.
