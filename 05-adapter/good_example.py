# good_example.py — Object adapter with Protocol
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Protocol


class PaymentMethod(StrEnum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"


CARD_NUMBERS: dict[PaymentMethod, str] = {
    PaymentMethod.VISA: "4111111111111111",
    PaymentMethod.MASTERCARD: "5500000000000004",
    PaymentMethod.AMEX: "340000000000009",
}


class PaymentProcessor(Protocol):
    def pay(self, amount: Decimal, method: PaymentMethod) -> str: ...


class LegacyPaymentGateway:
    """Third-party gateway — cannot be modified."""

    def process_payment(self, amount_cents: int, card_number: str) -> str:
        return f"charged {amount_cents}c to card {card_number[-4:]}"


@dataclass(frozen=True)
class PaymentGatewayAdapter:
    """Translates PaymentProcessor calls into LegacyPaymentGateway calls."""

    _gateway: LegacyPaymentGateway

    def pay(self, amount: Decimal, method: PaymentMethod) -> str:
        cents = int(amount * 100)
        card = CARD_NUMBERS[method]
        return self._gateway.process_payment(cents, card)


def checkout(processor: PaymentProcessor, total: Decimal, method: PaymentMethod) -> str:
    return processor.pay(total, method)


if __name__ == "__main__":
    adapter = PaymentGatewayAdapter(LegacyPaymentGateway())
    result = checkout(adapter, Decimal("49.99"), PaymentMethod.VISA)
    print(result)
