"""
Generates a SYNTHETIC stand-in dataset that mirrors the column names, messiness,
and value formats of the real Kaggle dataset:
https://www.kaggle.com/datasets/juhibhojani/house-price

This repo ships with this synthetic file so the notebook / backend / frontend
all run end-to-end out of the box. Replace house_prices.csv with the REAL
Kaggle file before you submit your assignment (see README "Phase 1").
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 8000

cities = ["Mumbai", "Pune", "Bangalore", "Delhi", "Noida", "Gurgaon", "Chennai",
          "Hyderabad", "Kolkata", "Ahmedabad", "Thane", "Navi Mumbai", "Faridabad",
          "Ghaziabad", "Lucknow"]
localities = ["Sector {}".format(i) for i in range(1, 60)] + \
             ["{} Nagar".format(n) for n in ["Gandhi", "Shastri", "Indira", "Rajiv", "Model", "Green"]] + \
             ["Phase {}".format(i) for i in range(1, 10)]

furnishing_opts = ["Furnished", "Semi-Furnished", "Unfurnished"]
transaction_opts = ["New Property", "Resale"]
ownership_opts = ["Freehold", "Leasehold", "Co-operative Society", "Power of Attorney"]
facing_opts = ["East", "West", "North", "South", "North-East", "South-West", np.nan]
status_opts = ["Ready to Move", "Under Construction"]

def make_area_str(sqft):
    if rng.random() < 0.5:
        return f"{int(sqft)} sqft"
    else:
        sqm = sqft / 10.764
        return f"{sqm:.1f} sqm"

def make_price_str(price_rupees):
    r = rng.random()
    if r < 0.03:
        return "Call for Price"
    if price_rupees >= 1e7:
        return f"{price_rupees/1e7:.2f} Cr"
    else:
        return f"{price_rupees/1e5:.1f} Lac"

def make_floor_str():
    total = int(rng.integers(1, 25))
    cur = rng.integers(-1, total + 1)
    if cur == -1:
        return f"Basement out of {total}"
    if cur == 0:
        return f"Ground out of {total}"
    return f"{cur} out of {total}"

rows = []
for i in range(N):
    city = rng.choice(cities)
    locality = rng.choice(localities)
    location = f"{locality}, {city}"
    society = rng.choice([f"Society {j}" for j in range(1, 400)] + [np.nan])

    base_sqft = rng.normal(1300, 550)
    base_sqft = max(250, base_sqft)
    carpet_sqft = base_sqft * rng.uniform(0.75, 0.95)
    super_sqft = base_sqft * rng.uniform(1.0, 1.2)

    bathroom = int(np.clip(rng.poisson(2), 1, 6))
    balcony = int(np.clip(rng.poisson(1.2), 0, 4))
    car_parking = int(np.clip(rng.poisson(1), 0, 3))

    # price roughly driven by area + city tier + bathrooms, with noise
    city_multiplier = {"Mumbai": 2.6, "Delhi": 2.1, "Gurgaon": 2.0, "Bangalore": 1.8,
                        "Pune": 1.5, "Hyderabad": 1.5, "Chennai": 1.4, "Noida": 1.4,
                        "Navi Mumbai": 1.9, "Thane": 1.7, "Kolkata": 1.2,
                        "Ahmedabad": 1.1, "Faridabad": 1.1, "Ghaziabad": 1.0,
                        "Lucknow": 0.9}[city]
    price_per_sqft = rng.normal(4500, 1200) * city_multiplier
    price_per_sqft = max(800, price_per_sqft)
    price = base_sqft * price_per_sqft * (1 + 0.06 * bathroom) * rng.uniform(0.85, 1.15)

    # inject some outliers
    if rng.random() < 0.01:
        price *= rng.uniform(5, 12)
    if rng.random() < 0.005:
        price *= rng.uniform(0.05, 0.2)

    missing_mask = rng.random()

    row = {
        "Index": i,
        "Title": f"{int(np.clip(rng.normal(3, 1), 1, 6))} BHK Flat in {location}",
        "Description": "Well maintained property, close to schools and markets." if rng.random() > 0.3 else np.nan,
        "Amount(in rupees)": make_price_str(price) if missing_mask > 0.01 else np.nan,
        "Price (in rupees)": round(price, -3),
        "location": location if rng.random() > 0.02 else np.nan,
        "Carpet Area": make_area_str(carpet_sqft) if rng.random() > 0.15 else np.nan,
        "Status": rng.choice(status_opts),
        "Floor": make_floor_str() if rng.random() > 0.1 else np.nan,
        "Transaction": rng.choice(transaction_opts),
        "Furnishing": rng.choice(furnishing_opts) if rng.random() > 0.1 else np.nan,
        "facing": rng.choice(facing_opts),
        "overlooking": rng.choice(["Garden/Park", "Main Road", "Pool", np.nan]),
        "Society": society,
        "Bathroom": bathroom if rng.random() > 0.05 else np.nan,
        "Balcony": balcony if rng.random() > 0.2 else np.nan,
        "Car Parking": car_parking if rng.random() > 0.3 else np.nan,
        "Ownership": rng.choice(ownership_opts) if rng.random() > 0.2 else np.nan,
        "Super Area": make_area_str(super_sqft) if rng.random() > 0.4 else np.nan,
        "Dimensions": np.nan,
        "Plot Area": np.nan,
    }
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("house_prices.csv", index=False)
print("Wrote", len(df), "rows to house_prices.csv")
print(df.head())
