import math
from scipy.stats import norm
from scipy.optimize import brentq
from datetime import datetime

def black_scholes_price(S, K, T, r, q, sigma, option_type='call'):
    if T <= 0:
        if option_type == 'call':
            return max(S - K, 0)
        else:
            return max(K - S, 0)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == 'call':
        price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)
    return price

def implied_volatility(option_price, S, K, T, r, q, option_type='call'):
    def objective(sigma):
        return black_scholes_price(S, K, T, r, q, sigma, option_type) - option_price
    try:
        return brentq(objective, 0.001, 10.0)
    except ValueError:
        return None

def calculate_time_to_expiry(val_date, exp_date):
    if isinstance(val_date, str):
        val_date = datetime.strptime(val_date, "%Y-%m-%d")
    if isinstance(exp_date, str):
        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")
    return (exp_date - val_date).days / 365.0

def format_vol(iv):
    return "N/A" if iv is None else f"{iv * 100:.2f}%"

def main():
    print("=" * 60)
    print("  OPTIONS IMPLIED VOLATILITY CALCULATOR")
    print("=" * 60)
    print()
    ticker = input("Ticker: ").upper().strip()
    exp_date = input("Expiration date (YYYY-MM-DD): ")
    K = float(input("Strike price: $"))
    option_type = input("Option type (call/put): ").lower().strip()
    val_date = input("Valuation date (YYYY-MM-DD): ")
    S = float(input("Underlying price: $"))
    r = float(input("Risk-free rate (e.g., 0.05 for 5%): "))
    q = float(input("Dividend yield (e.g., 0.01 for 1%): "))
    price_a = float(input("Option price A: $"))
    price_b_input = input("Option price B (or Enter to skip): $").strip()
    price_b = float(price_b_input) if price_b_input else None
    price_c_input = input("Option price C (or Enter to skip): $").strip()
    price_c = float(price_c_input) if price_c_input else None
    T = calculate_time_to_expiry(val_date, exp_date)
    if T <= 0:
        print("\nError: Expiration date must be after valuation date.")
        return
    vol_a = implied_volatility(price_a, S, K, T, r, q, option_type)
    vol_b = implied_volatility(price_b, S, K, T, r, q, option_type) if price_b else None
    vol_c = implied_volatility(price_c, S, K, T, r, q, option_type) if price_c else None
    option_desc = f"{ticker} {exp_date} {K:.0f} {option_type.upper()}"
    print()
    print("=" * 100)
    print("  RESULTS")
    print("=" * 100)
    headers = ["Option", "Val Date", "Underlying", "r", "Div", "Price A", "Vol A"]
    values = [option_desc, val_date, f"${S:.2f}", f"{r*100:.2f}%", f"{q*100:.2f}%", f"${price_a:.2f}", format_vol(vol_a)]
    if price_b is not None:
        headers.extend(["Price B", "Vol B"])
        values.extend([f"${price_b:.2f}", format_vol(vol_b)])
    if price_c is not None:
        headers.extend(["Price C", "Vol C"])
        values.extend([f"${price_c:.2f}", format_vol(vol_c)])
    widths = [max(len(h), len(v)) + 2 for h, v in zip(headers, values)]
    header_row = "|".join(h.center(w) for h, w in zip(headers, widths))
    separator = "+".join("-" * w for w in widths)
    print(separator)
    print(header_row)
    print(separator)
    value_row = "|".join(v.center(w) for v, w in zip(values, widths))
    print(value_row)
    print(separator)

if __name__ == "__main__":
    main()
