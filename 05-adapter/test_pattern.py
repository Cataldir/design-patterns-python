# test_adapter.py — Verify the adapter translates correctly
from decimal import Decimal

import pytest

from good_example import (
    LegacyPaymentGateway,
    PaymentGatewayAdapter,
    PaymentMethod,
)


@pytest.fixture
def adapter() -> PaymentGatewayAdapter:
    return PaymentGatewayAdapter(LegacyPaymentGateway())


def test_converts_decimal_to_cents(adapter: PaymentGatewayAdapter) -> None:
    result = adapter.pay(Decimal("29.99"), PaymentMethod.VISA)
    assert "2999c" in result


def test_masks_card_number(adapter: PaymentGatewayAdapter) -> None:
    result = adapter.pay(Decimal("10.00"), PaymentMethod.MASTERCARD)
    assert "0004" in result
    assert "5500000000000004" not in result


def test_all_payment_methods_accepted(adapter: PaymentGatewayAdapter) -> None:
    for method in PaymentMethod:
        result = adapter.pay(Decimal("1.00"), method)
        assert "charged" in result
