from __future__ import annotations

import argparse
from typing import List

from app.ingest import DocumentSource, ingest_sources, merge_documents


RISK_HINTS = {
    "arbitration": ["arbitration", "class action waiver", "dispute resolution"],
    "auto_renewal": ["auto-renew", "auto renew", "recurring", "subscription"],
    "privacy_sharing": ["third party", "share", "sell", "advertising partners"],
    "liability_limits": ["limitation of liability", "not liable", "as is"],
    "termination": ["terminate", "suspend", "without notice"],
}


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    sources = _collect_sources(args.text, args.file, args.url)
    if not sources:
        parser.error("Provide at least one input via --text, --file, or --url")

    documents = ingest_sources(sources)
    merged = merge_documents(documents)

    report = summarize_terms(merged)
    print(report)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest terms from multiple sources and summarize them."
    )
    parser.add_argument(
        "--text",
        action="append",
        default=[],
        help="Inline terms text. Can be passed multiple times.",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Path to local document file (.txt/.md). Can be passed multiple times.",
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Remote URL containing terms. Can be passed multiple times.",
    )
    return parser


def _collect_sources(
    text_inputs: List[str], file_inputs: List[str], url_inputs: List[str]
) -> List[DocumentSource]:
    sources: List[DocumentSource] = []
    for item in text_inputs:
        sources.append(DocumentSource(source_type="text", value=item))
    for item in file_inputs:
        sources.append(DocumentSource(source_type="file", value=item))
    for item in url_inputs:
        sources.append(DocumentSource(source_type="url", value=item))
    return sources


def summarize_terms(merged_text: str) -> str:
    """
    Placeholder summarizer.
    Replace this with LLM-backed extraction/summarization in next iteration.
    """
    text_lower = merged_text.lower()
    flagged = []

    for label, phrases in RISK_HINTS.items():
        if any(phrase in text_lower for phrase in phrases):
            flagged.append(label)

    preview = merged_text[:800].strip()
    if len(merged_text) > 800:
        preview += "..."

    lines = [
        "Conditional Terms Summary",
        "=========================",
        "",
        f"Input size: {len(merged_text)} characters",
        f"Potentially relevant categories: {', '.join(flagged) if flagged else 'none detected'}",
        "",
        "Preview:",
        preview or "(empty input)",
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    main()