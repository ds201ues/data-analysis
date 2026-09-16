"""
Generate a realistic Indian media company advertising sales dataset
for the BCCL data analytics training session.

Features:
- 2000+ rows, 3 years of data
- Multiple dimensions: city, edition, ad_type, category, sales_rep
- Multiple measures: revenue, pages, rate, discount
- Built-in patterns: trends, seasonality, segments, outliers
- Indian context: cities, ₹ amounts, BCCL-like structure
"""

import csv
import random
import datetime
from collections import defaultdict

random.seed(42)

# --- Dimensions ---
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
editions = ['Times of India', 'Economic Times', 'Navbharat Times', 'Maharashtra Times']
ad_types = ['Display', 'Classified', 'Supplement', 'Digital', 'Branded Content']
categories = ['Real Estate', 'Automobile', 'Education', 'BFSI', 'FMCG', 'Retail', 'Tech', 'Healthcare', 'Government', 'Matrimonial']
sales_reps = [f'SR{str(i).zfill(3)}' for i in range(1, 31)]

# Rate cards (₹ per sq cm or per unit)
base_rates = {
    'Display': 3500,
    'Classified': 800,
    'Supplement': 2200,
    'Digital': 150,  # per 1000 impressions (CPM)
    'Branded Content': 50000,  # per piece
}

city_multiplier = {
    'Mumbai': 1.4, 'Delhi': 1.3, 'Bangalore': 1.1, 'Chennai': 0.9,
    'Kolkata': 0.8, 'Hyderabad': 0.95, 'Pune': 0.85, 'Ahmedabad': 0.75
}

edition_multiplier = {
    'Times of India': 1.3, 'Economic Times': 1.1,
    'Navbharat Times': 0.7, 'Maharashtra Times': 0.6
}

# Seasonal pattern (Indian market: Q4 Jan-Mar strong, Diwali Oct-Nov, monsoon Jul-Aug weak)
month_seasonality = {
    1: 1.15, 2: 1.10, 3: 1.20,  # Q4 (Indian FY) - strong
    4: 0.90, 5: 0.85, 6: 0.80,  # Q1 - post year-end
    7: 0.75, 8: 0.78, 9: 0.95,  # Monsoon weak, Sep recovery
    10: 1.25, 11: 1.35, 12: 1.05  # Diwali + festive peak
}

# Year trends (print declining, digital growing)
year_trend = {
    2022: {'Display': 1.0, 'Classified': 1.0, 'Supplement': 1.0, 'Digital': 1.0, 'Branded Content': 1.0},
    2023: {'Display': 0.95, 'Classified': 0.85, 'Supplement': 0.92, 'Digital': 1.40, 'Branded Content': 1.25},
    2024: {'Display': 0.88, 'Classified': 0.70, 'Supplement': 0.85, 'Digital': 1.90, 'Branded Content': 1.55},
}

rows = []
order_id = 10001

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2024, 12, 31)

current = start_date
while current <= end_date:
    # Number of bookings per day (varies by day of week and season)
    base_bookings = 4 if current.weekday() < 5 else 1
    seasonal = month_seasonality[current.month]
    n_bookings = max(1, int(base_bookings * seasonal * random.uniform(0.6, 1.4)))

    for _ in range(n_bookings):
        city = random.choice(cities)
        edition = random.choice(editions)
        ad_type = random.choices(
            ad_types,
            weights=[30, 25, 15, 20, 10],  # Display most common
            k=1
        )[0]
        category = random.choice(categories)
        rep = random.choice(sales_reps)

        # Calculate rate
        base = base_rates[ad_type]
        rate = base * city_multiplier[city] * edition_multiplier[edition]
        rate *= year_trend[current.year][ad_type]
        rate *= random.uniform(0.8, 1.2)  # noise

        # Quantity (sq cm for print, impressions/1000 for digital, pieces for branded)
        if ad_type == 'Digital':
            quantity = random.choice([50, 100, 200, 500, 1000])  # thousands of impressions
        elif ad_type == 'Branded Content':
            quantity = random.randint(1, 4)
        elif ad_type == 'Classified':
            quantity = random.randint(5, 50)  # small
        else:
            quantity = random.choice([20, 40, 60, 80, 100, 120, 150, 200, 250, 300])

        # Discount (larger clients get more)
        discount_pct = random.choices(
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            weights=[10, 15, 20, 15, 15, 10, 5, 4, 3, 2, 1],
            k=1
        )[0]

        # Gross and net
        gross = round(rate * quantity * seasonal, 2)
        net = round(gross * (1 - discount_pct/100), 2)

        # Status
        status = random.choices(
            ['Confirmed', 'Cancelled', 'Pending'],
            weights=[80, 12, 8],
            k=1
        )[0]

        rows.append({
            'order_id': f'ORD-{order_id}',
            'booking_date': current.strftime('%Y-%m-%d'),
            'publish_date': (current + datetime.timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d'),
            'city': city,
            'edition': edition,
            'ad_type': ad_type,
            'category': category,
            'sales_rep': rep,
            'quantity': quantity,
            'rate_per_unit': round(rate, 2),
            'discount_pct': discount_pct,
            'gross_amount': gross,
            'net_amount': net,
            'status': status,
        })
        order_id += 1

    current += datetime.timedelta(days=1)

# --- Add outliers/anomalies ---
# A few very large deals
for _ in range(8):
    idx = random.randint(0, len(rows)-1)
    rows[idx]['gross_amount'] *= 15
    rows[idx]['net_amount'] = rows[idx]['gross_amount'] * 0.6
    rows[idx]['quantity'] *= 10
    rows[idx]['category'] = random.choice(['Real Estate', 'Government', 'BFSI'])

# A few data quality issues (realistic)
for _ in range(15):
    idx = random.randint(0, len(rows)-1)
    rows[idx]['city'] = random.choice(['mumbai', 'MUMBAI', 'Mumabi', 'Delhi ', ' Delhi'])  # typos

for _ in range(10):
    idx = random.randint(0, len(rows)-1)
    rows[idx]['net_amount'] = ''  # missing values

for _ in range(5):
    idx = random.randint(0, len(rows)-1)
    rows[idx]['discount_pct'] = 95  # suspicious deep discounts

# --- Write CSV ---
output_path = '/Users/dishantsingla/Downloads/session-data/ad-sales-data.csv'
fieldnames = ['order_id', 'booking_date', 'publish_date', 'city', 'edition',
              'ad_type', 'category', 'sales_rep', 'quantity', 'rate_per_unit',
              'discount_pct', 'gross_amount', 'net_amount', 'status']

with open(output_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows")
print(f"Date range: {rows[0]['booking_date']} to {rows[-1]['booking_date']}")
print(f"Saved to: {output_path}")

# Quick stats
confirmed = [r for r in rows if r['status'] == 'Confirmed']
net_vals = [r['net_amount'] for r in confirmed if r['net_amount'] != '']
print(f"\nConfirmed orders: {len(confirmed)}")
print(f"Total net revenue: ₹{sum(float(v) for v in net_vals)/10000000:.1f} Cr (approx)")
print(f"Cities: {len(set(r['city'] for r in rows))}")
print(f"Unique dates: {len(set(r['booking_date'] for r in rows))}")
