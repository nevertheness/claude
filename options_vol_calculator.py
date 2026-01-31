import math
from scipy.stats import norm
from scipy.optimize import brentq
from datetime import datetime

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price.

    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate (annual)
    sigma: Volatility (annual)
    option_type: 'call' or 'put'
    """
    if T <= 0:
        # At expiration
        if option_type == 'call':
            return max(S - K, 0)
        else:
            return max(K - S, 0)

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price


def implied_volatility(option_price, S, K, T, r, option_type='call'):
    """
    Calculate implied volatility using Brent's method.

    option_price: Market price of the option
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate (annual)
    option_type: 'call' or 'put'
    """
    def objective(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - option_price

    try:
        # Search for IV between 0.1% and 500%
        iv = brentq(objective, 0.001, 5.0)
        return iv
    except ValueError:
        return None


def calculate_time_to_expiry(val_date, exp_date):
    """Calculate time to expiry in years."""
    if isinstance(val_date, str):
        val_date = datetime.strptime(val_date, "%Y-%m-%d")
    if isinstance(exp_date, str):
        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")

    days = (exp_date - val_date).days
    return days / 365.0


def main():
    print("=" * 50)
    print("  OPTIONS IMPLIED VOLATILITY CALCULATOR")
    print("=" * 50)
    print()

    # Get inputs
    S = float(input("Stock price: $"))
    K = float(input("Strike price: $"))
    option_price = float(input("Option price: $"))
    option_type = input("Option type (call/put): ").lower().strip()
    val_date = input("Valuation date (YYYY-MM-DD): ")
    exp_date = input("Expiration date (YYYY-MM-DD): ")
    r = float(input("Risk-free rate (e.g., 0.05 for 5%): "))

    # Calculate time to expiry
    T = calculate_time_to_expiry(val_date, exp_date)

    if T <= 0:
        print("\nError: Expiration date must be after valuation date.")
        return

    # Calculate implied volatility
    iv = implied_volatility(option_price, S, K, T, r, option_type)

    print()
    print("=" * 50)
    print("  RESULTS")
    print("=" * 50)
    print(f"Stock Price:      ${S:.2f}")
    print(f"Strike Price:     ${K:.2f}")
    print(f"Option Price:     ${option_price:.2f}")
    print(f"Option Type:      {option_type.upper()}")
    print(f"Days to Expiry:   {int(T * 365)}")
    print(f"Time to Expiry:   {T:.4f} years")
    print(f"Risk-Free Rate:   {r*100:.2f}%")
    print("-" * 50)

    if iv is not None:
        print(f"IMPLIED VOLATILITY: {iv*100:.2f}%")

        # Verify by calculating price with IV
        verify_price = black_scholes_price(S, K, T, r, iv, option_type)
        print(f"Verified Price:     ${verify_price:.2f}")
    else:
        print("Could not calculate implied volatility.")
        print("Check that the option price is within valid bounds.")


if __name__ == "__main__":
    main()
