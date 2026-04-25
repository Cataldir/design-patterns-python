# solution.py — Strategy-based return eligibility validation
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


class WithinReturnWindow:
    def is_eligible(self, request: ReturnRequest) -> bool:
        return (request.request_date - request.order_date) <= timedelta(days=30)

    def rejection_reason(self) -> str:
        return "Return window (30 days) has expired."


class ItemNotDamaged:
    def is_eligible(self, request: ReturnRequest) -> bool:
        return request.item_condition != "damaged"

    def rejection_reason(self) -> str:
        return "Damaged items are not eligible for return."


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


if __name__ == "__main__":
    request = ReturnRequest(
        order_date=datetime.now() - timedelta(days=10),
        request_date=datetime.now(),
        item_condition="new",
        reason="Changed my mind",
    )
    rules: list[EligibilityRule] = [WithinReturnWindow(), ItemNotDamaged()]
    eligible, reasons = validate_return(request, rules)
    print(f"Eligible: {eligible}, Reasons: {reasons}")
