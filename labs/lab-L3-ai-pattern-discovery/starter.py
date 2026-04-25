# starter.py — Return eligibility skeleton (fill in the rules)
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol


@dataclass(frozen=True)
class ReturnRequest:
    order_date: datetime
    request_date: datetime
    item_condition: str  # "new", "used", "damaged"
    reason: str


class EligibilityRule(Protocol):
    def is_eligible(self, request: ReturnRequest) -> bool: ...
    def rejection_reason(self) -> str: ...


# TODO: Implement WithinReturnWindow rule (30-day window)
# TODO: Implement ItemNotDamaged rule


def validate_return(
    request: ReturnRequest,
    rules: list[EligibilityRule],
) -> tuple[bool, list[str]]:
    rejections = [
        rule.rejection_reason()
        for rule in rules
        if not rule.is_eligible(request)
    ]
    return (len(rejections) == 0, rejections)
