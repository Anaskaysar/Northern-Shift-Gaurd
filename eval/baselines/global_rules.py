"""Baseline B1: Global rules — hard hat + hi-vis always required."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ComplianceResult:
    overall: str  # "compliant" | "non_compliant"
    false_alarm: bool  # True if flagged non-compliant when ground truth is compliant


GLOBAL_REQUIRED = {"hard_hat", "hi_vis"}


def evaluate_global(
    hard_hat: str,
    hi_vis: str,
    ground_truth_compliant: bool,
) -> ComplianceResult:
    """Global baseline: both hard hat and hi-vis always required."""
    compliant = hard_hat == "pass" and hi_vis == "pass"
    overall = "compliant" if compliant else "non_compliant"
    false_alarm = overall == "non_compliant" and ground_truth_compliant
    return ComplianceResult(overall=overall, false_alarm=false_alarm)
