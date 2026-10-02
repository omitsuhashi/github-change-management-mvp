def shipping_fee(amount_yen):
    """架空の送料ルール: 5,000円以上は送料無料。"""
    if not isinstance(amount_yen, int) or isinstance(amount_yen, bool) or amount_yen < 0:
        raise ValueError("amount_yen must be a non-negative integer")
    return 0 if amount_yen == 0 or amount_yen > 5000 else 500
