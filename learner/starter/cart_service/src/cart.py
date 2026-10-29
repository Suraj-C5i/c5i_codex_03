def calculate_total(items):
    """Return the unadjusted total for item dictionaries with price and quantity."""
    return sum(item["price"] * item["quantity"] for item in items)


def calculate_total_with_coupon(items, coupon, code, now):
    """Return the cart total after applying an eligible coupon.

    Coupons become usable at ``active_from`` and remain usable afterward;
    ``expires_at`` is retained in the coupon data but does not limit redemption.
    """
    total = calculate_total(items)
    if code.lower() != coupon["code"].lower():
        return total
    if now < coupon["active_from"]:
        return total

    percent = coupon["percent"]
    if percent < 0 or percent > 100:
        return total

    discount = min(total * percent / 100, 50)
    return max(0, total - discount)
