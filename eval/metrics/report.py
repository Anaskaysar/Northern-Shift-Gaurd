"""Evaluation metrics for Northern Shift Guard research paper."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PPEMetrics:
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    true_negatives: int = 0

    @property
    def precision(self) -> float:
        denom = self.true_positives + self.false_positives
        return self.true_positives / denom if denom else 0.0

    @property
    def recall(self) -> float:
        denom = self.true_positives + self.false_negatives
        return self.true_positives / denom if denom else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0


@dataclass
class EvalReport:
    total_images: int = 0
    zone_flip_cases: int = 0
    global_false_alarms: int = 0
    zone_aware_false_alarms: int = 0
    zone_flip_correct: int = 0
    hard_hat_metrics: PPEMetrics = field(default_factory=PPEMetrics)
    hi_vis_metrics: PPEMetrics = field(default_factory=PPEMetrics)

    @property
    def false_alarm_reduction_pct(self) -> float:
        if self.global_false_alarms == 0:
            return 0.0
        reduced = self.global_false_alarms - self.zone_aware_false_alarms
        return 100.0 * reduced / self.global_false_alarms

    @property
    def zone_flip_accuracy(self) -> float:
        if self.zone_flip_cases == 0:
            return 0.0
        return self.zone_flip_correct / self.zone_flip_cases

    def to_dict(self) -> dict:
        return {
            "total_images": self.total_images,
            "zone_flip_cases": self.zone_flip_cases,
            "global_false_alarms": self.global_false_alarms,
            "zone_aware_false_alarms": self.zone_aware_false_alarms,
            "false_alarm_reduction_pct": round(self.false_alarm_reduction_pct, 1),
            "zone_flip_accuracy": round(self.zone_flip_accuracy, 3),
            "hard_hat": {
                "precision": round(self.hard_hat_metrics.precision, 3),
                "recall": round(self.hard_hat_metrics.recall, 3),
                "f1": round(self.hard_hat_metrics.f1, 3),
            },
            "hi_vis": {
                "precision": round(self.hi_vis_metrics.precision, 3),
                "recall": round(self.hi_vis_metrics.recall, 3),
                "f1": round(self.hi_vis_metrics.f1, 3),
            },
        }
