import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

file_path = os.path.join(os.getcwd(), 'ecommerce_data.csv')

# قائمة مدن موسعة لضبط الخريطة
location_pool = [
    {'City': 'Halifax', 'Country': 'Canada', 'Lat': 44.6488, 'Lon': -63.5752},
    {'City': 'Dartmouth', 'Country': 'Canada', 'Lat': 44.6662, 'Lon': -63.5682},
    {'City': 'Toronto', 'Country': 'Canada', 'Lat': 43.6532, 'Lon': -79.3832},
    {'City': 'Vancouver', 'Country': 'Canada', 'Lat': 49.2827, 'Lon': -123.1207},
    {'City': 'New York', 'Country': 'United States', 'Lat': 40.7128, 'Lon': -74.0060},
    {'City': 'Miami', 'Country': 'United States', 'Lat': 25.7617, 'Lon': -80.1918}
]

data_list = []
categories = {
    'Data Analytics': ['Server Rack', 'Quantivo AI License', 'BI Dashboard Pro'],
    'Tech Support': ['24/7 Support', 'Cloud Migration'],
    'Apparel': ['ME-U Hoodie', 'Streetwear Cap']
}

for _ in range(5000):
    parent_cat = np.random.choice(list(categories.keys()))
    sub_cat = np.random.choice(categories[parent_cat])
    loc = np.random.choice(location_pool)
    
    sales = np.random.uniform(1000, 25000)
    # زيادة نسبة الربح لتكون بين 20% لـ 50% بناءً على طلبك
    profit_margin = np.random.uniform(0.20, 0.50) 
    profit = sales * profit_margin
    
    data_list.append({
        'Date': datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 400)),
        'City': loc['City'],
        'Country': loc['Country'],
        'Parent_Category': parent_cat,
        'Sub_Category': sub_cat,
        'Sales': sales,
        'Profit': profit,
        'Lat': loc['Lat'],
        'Lon': loc['Lon']
    })

df = pd.DataFrame(data_list)
df.to_csv(file_path, index=False)
print(f"✅ Data generated with higher profits at: {file_path}")