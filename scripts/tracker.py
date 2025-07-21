import pandas as pd
import requests
from datetime import datetime

# Load CSV
df = pd.read_csv('data/investments.csv')


def fetch_gold_price_usd():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": "goldapi-6x1cs5smdcyyif6-io",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # You get the gold price per ounce in USD
    return data['price_gram_24k']

def convert_usd_to_pkr(usd_amount):
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    rate = response.json()["rates"]["PKR"]
    return usd_amount * rate

gold_usd = fetch_gold_price_usd()
gold_pkr = convert_usd_to_pkr(gold_usd)

print(f"Gold Price per ounce: ${gold_usd:.2f}")
print(f"Gold Price in PKR: Rs {gold_pkr:,.0f}")
# Fetch live prices
def fetch_price(asset):
    if asset in ["USD", "EUR"]:
        url = f'https://v6.exchangerate-api.com/v6/33446f9a63cee8fe4f9654fb/latest/{asset}'
        try:
            response = requests.get(url)
            data = response.json()
            return data.get('conversion_rates', {}).get('PKR', None)
        except Exception as e:
            print(f"❌ Error fetching {asset}: {e}")
            return None

    elif asset == "Gold":
        return gold_pkr  # ✅ Use pre-fetched PKR gold price per gram

    return None


# Create report
report = f"## 📊 Daily Investment Report - {datetime.now().strftime('%B %d, %Y')}\n\n"
report += "| Asset | Quantity | Buy Price | Current Price | Gain/Loss | % Change |\n"
report += "|-------|----------|-----------|----------------|------------|----------|\n"

for _, row in df.iterrows():
    current_price = fetch_price(row['asset'])
    if current_price is None:
        print(f"⚠️ Skipping {row['asset']} — price not available")
        continue

    total_buy = row['buy_price'] * row['quantity']
    total_current = current_price * row['quantity']
    gain_loss = total_current - total_buy
    percent_change = (gain_loss / total_buy) * 100

    report += f"| {row['asset']} | {row['quantity']} | {row['buy_price']} PKR | {round(current_price,2)} PKR | {round(gain_loss,2)} PKR | {round(percent_change,2)}% |\n"



# Write report to markdown
with open("report.md", "w") as f:
    f.write(report)

print("✅ Report generated.")
