# bad_example.py — Caller coupled directly to a legacy payment interface
from decimal import Decimal
from enum import StrEnum


class PaymentMethod(StrEnum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"


class LegacyPaymentGateway:
    """Third-party gateway — you cannot modify this class."""

    def process_payment(self, amount_cents: int, card_number: str) -> str:
        return f"charged {amount_cents}c to card {card_number[-4:]}"


def checkout(total: Decimal, method: PaymentMethod) -> str:
    gateway = LegacyPaymentGateway()
    cents = int(total * 100)
    card = {"visa": "4111111111111111", "mastercard": "5500000000000004",
            "amex": "340000000000009"}[method.value]
    return gateway.process_payment(cents, card)


if __name__ == "__main__":
    result = checkout(Decimal("49.99"), PaymentMethod.VISA)
    print(result)
