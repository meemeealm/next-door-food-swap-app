import sqlite3
import random
from datetime import datetime, timedelta
from database import db_path, init_db

# Sample data for randomization
# Names (Mix of PH, MY, ID, SG vibes)
NAMES = [
    "Siti", "Jun", "Mateo", "Linh", "Budi", 
    "Apinya", "Ramesh", "Maria", "Taufik", "Santi"
]

# Items (SEA Staples)
ITEMS = {
    "Vegetables": ["Eggplant (Talong)", "Bitter Gourd (Ampalaya)", "Kangkong", "Bok Choy", "Okra"],
    "Fruit": ["Mangoes (Carabao)", "Durian", "Calamansi", "Rambutan", "Papaya"],
    "Cooked Meal": ["Adobo", "Nasi Lemak", "Pad Thai", "Beef Rendang", "Pancit Canton"],
    "Herbs": ["Lemongrass", "Pandan Leaves", "Thai Basil", "Turmeric", "Curry Leaves"],
    "Other": ["Ube Halaya", "Coconut Milk", "Sambal Paste", "Fish Sauce", "Salted Eggs"]
}

# Quantities (Local phrasing)
QUANTITIES = ["1 kg", "3 bundles", "1 tupperware", "5 pieces", "1 bowl", "Small plastic bag"]

def seed_database(num_entries=10):
    # Ensure the table exists first
    init_db()
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    print(f"Generating {num_entries} random food items...")
    
    for _ in range(num_entries):
        user = random.choice(NAMES)
        phone = f"1{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        category = random.choice(list(ITEMS.keys()))
        item = random.choice(ITEMS[category])
        qty = random.choice(QUANTITIES)
        
        # Create a random date within the last 3 days
        random_days = random.randint(0, 3)
        random_date = (datetime.now() - timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M")

        c.execute('''
            INSERT INTO food_items (user, phone, item, category, quantity, posted, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (user, phone, item, category, qty, random_date, 'Available')
        )
    
    conn.commit()
    conn.close()
    print("✅ Success! Database is now seeded with fresh food.")

if __name__ == "__main__":
    seed_database(40) # Change this number for more or less data