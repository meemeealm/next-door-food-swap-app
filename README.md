### 🍎 NextDoor: Neighborhood Food Swapping App  

A localized, community-driven web application designed to reduce food waste and strengthen neighborhood ties. This app allows residents to post extra garden harvests, pantry items, or home-cooked meals for their neighbors to claim.

### 📸 App Preview

| <img src="https://github.com/meemeealm/next-door-food-swap-app/blob/main/imgs/nextdoor_home.png" width="45%"/> | <img src="https://github.com/meemeealm/next-door-food-swap-app/blob/main/imgs/nextdoor_map.png" width="45%"/> |

--- 

### ✨ Features

Localized Community Board: A neighborhood-first platform tailored for South East Asian staples—sharing everything from Adobo and Kangkong to Ube and Calamansi.

Persistent SQLite Backend: Robust data management using SQL, moving beyond temporary files to ensure community postings are safely stored and easily retrievable.

Intelligent Search & Categorization: High-performance filtering that allows neighbors to instantly sort through local produce and cooked meals by keyword or regional category.

Seamless WhatsApp Coordination: Direct-to-chat integration via custom-styled API links, featuring pre-filled messages to eliminate friction between neighbors.

Real-time Reservation Logic: A synchronized "Claim" system that updates the database instantly, marking items as "Reserved" across all user sessions to prevent double-claiming.

Geospatial Data Visualization: A high-performance Pydeck integration that renders color-coded categories across a dynamic map layer, featuring custom HTML tooltips and automated coordinate-clustering for localized neighborhood discovery.

Responsive UI: A modern, mobile-friendly interface powered by custom CSS, featuring a distinct color-coded action system:  
Action Blue: For claiming and contributing.  
WhatsApp Green: For instant regional communication.

---

### 🛠️ Tech Stack
Python 3.x

Streamlit (Frontend & State Management)

Pandas (Data Handling)

HTML/CSS (Custom UI Injection)

pydeck (map)

faker (Generate fake data)

---

### 🚀 How to Run
Clone this repository.

Install requirements: ``pip install streamlit pandas``.

Run the app: ``streamlit run app.py``.
