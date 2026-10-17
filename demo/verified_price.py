def effective_price(price, fallback):
    return fallback if price is None else price
