from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.policies import DEFAULT_RISK_POLICIES, RiskPolicy


@dataclass(frozen=True)
class RiskHit:
    key: str
    label: str
    description: str
    matched_keywords: List[str]


@dataclass(frozen=True)
class SummaryResult:
    input_chars: int
    highlights: List[RiskHit]
    preview: str


class HeuristicSummarizer:
    def __init__(self, policies: List[RiskPolicy] | None = None, preview_chars: int = 800):
        self.policies = policies or DEFAULT_RISK_POLICIES
        self.preview_chars = preview_chars

    def summarize(self, merged_text: str) -> SummaryResult:
        text_lower = merged_text.lower()
        highlights: List[RiskHit] = []

        for policy in self.policies:
            matched = [keyword for keyword in policy.keywords if keyword in text_lower]
            if matched:
                highlights.append(
                    RiskHit(
                        key=policy.key,
                        label=policy.label,
                        description=policy.description,
                        matched_keywords=matched,
                    )
                )

        preview = merged_text[: self.preview_chars].strip()
        if len(merged_text) > self.preview_chars:
            preview += "..."

        return SummaryResult(
            input_chars=len(merged_text),
            highlights=highlights,
            preview=preview or "(empty input)",
        )
