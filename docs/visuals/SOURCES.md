# Visual sources

These are report summaries and workflow diagrams, not screenshots of a web app.
Every customer name, source, contact and result in the example is fictional.
The visible notice must remain on the result card wherever it is reused.

- `workflow-en.svg` / `workflow-zh.svg`: the business steps in
  [SKILL.md](../../.agents/skills/foreign-customer-investigation/SKILL.md), the
  evidence states and validation contract in `scripts/models.py`, and the
  DOCX/XLSX/JSON generators. Research is performed by the host agent; the Python
  scripts validate an assembled report and produce files.
- `result-en.svg` / `result-zh.svg`: the committed
  [Aurora JSON fixture](../../examples/chinese-user-overseas-customer/FICTIONAL_Aurora_Printworks_investigation.json).
  The Chinese report is loaded through `InvestigationReport.model_validate`.
  English fields come from `examples/build_examples.py::make_report("a", EN)`;
  the generator reconciles the committed Chinese fixture and all score items.
- Five positive dimensions and risk deduction use the existing model. Bar
  lengths show points earned divided by that dimension's actual maximum;
  they do not show a probability or an independently measured customer outcome.
  Purchase potential is 14/15; risk deduction is −2. The model recomputes 97/100
  and derives A using its mandatory evidence conditions.
- Customer type, development value, purchase signals, products, maximum risk
  and priority action are existing report fields, without new commercial facts.
  Missing supplier, scale and equipment information stays missing in the full
  linked reports; the illustration is a small summary, not an additional inquiry.

Rebuild after installing the normal locked requirements:

```bash
python scripts/build_portfolio_visuals.py
python scripts/build_portfolio_visuals.py --check
```

The generator uses Python, Pydantic and SVG only. It does not fetch customer
information, invent scores, modify the scoring model or overwrite the original
example reports. `manifest.json` stores source and visual SHA-256 hashes, exact
dimension values, deduction, total and grade. CI checks reproducibility.

The SVGs use embedded styles, selectable text and no scripts or external assets.
English and Chinese versions show the same sample and numerical results.
