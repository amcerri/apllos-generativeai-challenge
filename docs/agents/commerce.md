# Commerce Agent

Covers document processor, extractor(s), and summarizer.

## Processor ([app/agents/commerce/processor.py](../../app/agents/commerce/processor.py))

- Input: attachment `{filename, content (bytes/base64 or text), mime_type}`.
- PDF: pypdf text extraction first; fallback to OCR via pdf2image + pytesseract.
- DOCX: python-docx paragraphs and tables.
- TXT: decoding with fallbacks.
- Images: PIL + optional OpenCV preprocessing for OCR.
- Output: `{text, metadata, method, warnings, success}`.

## LLM Extractor ([app/agents/commerce/extractor_llm.py](../../app/agents/commerce/extractor_llm.py))

- OpenAI JSON Schema structured extraction with business focus and risks; adds usage metadata.
- Prompt engineering with Chain-of-Thought reasoning and self-consistency checks.
- Fallback: heuristic extractor when LLM unavailable/errors.

## Heuristic Extractor ([app/agents/commerce/extractor.py](../../app/agents/commerce/extractor.py))

- Regex-based doc_id detection by type; currency detection; item line parsing with reconciliation for missing values.
- Totals parsing (subtotal, freight, discounts, grand total) + risk flags (sum mismatch, components mismatch).
- Produces canonical `CommerceDoc` dict.

## Summarizer ([app/agents/commerce/summarizer.py](../../app/agents/commerce/summarizer.py))

- PT-BR summary with document identity, totals, dates, top items (configurable counts), risks, and follow-ups.
- Confidence calibration for risk assessment and business insights.

---

**← [Back to Documentation Index](../README.md)**
