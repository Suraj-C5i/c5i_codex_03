import unittest
from datetime import datetime, timedelta, timezone

from src.cart import calculate_total, calculate_total_with_coupon

class CartContractTests(unittest.TestCase):
    def test_existing_total_contract(self):
        result = calculate_total([{"price": 5, "quantity": 2}, {"price": 3, "quantity": 1}])
        self.assertEqual(result, 13)
        self.assertIsInstance(result, (int, float))

    def test_empty_cart_is_zero(self):
        self.assertEqual(calculate_total([]), 0)


class CartCouponTests(unittest.TestCase):
    def setUp(self):
        self.items = [{"price": 100, "quantity": 1}]
        self.active_from = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.expires_at = self.active_from + timedelta(days=1)
        self.coupon = {
            "code": "SAVE20",
            "active_from": self.active_from,
            "expires_at": self.expires_at,
            "percent": 20,
        }

    def calculate_with_coupon(self, *, code="SAVE20", now=None, items=None, coupon=None):
        return calculate_total_with_coupon(
            self.items if items is None else items,
            self.coupon if coupon is None else coupon,
            code,
            self.active_from if now is None else now,
        )

    def test_coupon_code_matching_is_case_insensitive(self):
        self.assertEqual(self.calculate_with_coupon(code="save20"), 80)

    def test_nonmatching_code_returns_undiscounted_total(self):
        self.assertEqual(self.calculate_with_coupon(code="OTHER"), 100)

    def test_coupon_is_inactive_just_before_activation(self):
        now = self.active_from - timedelta(microseconds=1)
        self.assertEqual(self.calculate_with_coupon(now=now), 100)

    def test_coupon_is_active_at_activation(self):
        self.assertEqual(self.calculate_with_coupon(now=self.active_from), 80)

    def test_coupon_remains_active_at_expiry(self):
        self.assertEqual(self.calculate_with_coupon(now=self.expires_at), 80)

    def test_coupon_remains_active_after_expiry(self):
        now = self.expires_at + timedelta(days=30)
        self.assertEqual(self.calculate_with_coupon(now=now), 80)

    def test_zero_percent_coupon_has_no_discount(self):
        coupon = {**self.coupon, "percent": 0}
        self.assertEqual(self.calculate_with_coupon(coupon=coupon), 100)

    def test_invalid_percent_returns_undiscounted_total(self):
        for percent in (-1, 101):
            with self.subTest(percent=percent):
                coupon = {**self.coupon, "percent": percent}
                self.assertEqual(self.calculate_with_coupon(coupon=coupon), 100)

    def test_discount_is_capped_at_50(self):
        coupon = {**self.coupon, "percent": 100}
        items = [{"price": 120, "quantity": 1}]
        self.assertEqual(self.calculate_with_coupon(coupon=coupon, items=items), 70)

    def test_total_does_not_fall_below_zero(self):
        coupon = {**self.coupon, "percent": 100}
        items = [{"price": 20, "quantity": 1}]
        self.assertEqual(self.calculate_with_coupon(coupon=coupon, items=items), 0)

    def test_percentage_uses_full_precision_without_rounding(self):
        coupon = {**self.coupon, "percent": 33}
        items = [{"price": 10, "quantity": 1}]
        self.assertAlmostEqual(self.calculate_with_coupon(coupon=coupon, items=items), 6.7)

if __name__ == "__main__":
    unittest.main()
