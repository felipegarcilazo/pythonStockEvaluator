

# === SOTP VALUATION (manual inputs) ===
print("\n--- SOTP Valuation ---")
sotp_segments = {}
while True:
    segment = input("Enter segment name (or 'done' to finish): ")
    if segment.lower() == "done":
        break
    value = float(input(f"Enter value of {segment} ($B): ")) * 1e9
    sotp_segments[segment] = value

sotp_total_value = sum(sotp_segments.values()) + net_cash
fair_value_per_share_sotp = sotp_total_value / shares_outstanding

print(f"\nTotal SOTP Value: ${sotp_total_value / 1e9:.2f}B")
print(f"Fair Value per Share (SOTP): ${fair_value_per_share_sotp:.2f}")