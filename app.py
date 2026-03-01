import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. Setup the "Database"
DB_FILE = "food_swap_db.csv"

def load_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["User", "Phone", "Item", "Category", "Quantity", "Posted"])
    df = pd.read_csv(DB_FILE)
    return df.reset_index(drop=True) 

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# 2. Page Configuration
st.set_page_config(page_title="Neighborhood Food Swap", page_icon="🍎")
st.title("🍎 NextDoor")

# --- CUSTOM CSS ---
st.markdown("""
    
            
<style>
    /* Remove default Streamlit padding from columns */
    [data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Force all buttons to same height and remove top margins */
    .stButton, .wa-btn {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        width: 100% !important;
    }

    /* Style for both Streamlit buttons and the Link button */
    /* Ensure both button types have the exact same structural footprint */
    .claim-btn div.stButton > button, 
    .wa-btn {
        height: 42px !important;
        line-height: 42px !important; /* Centers text vertically in the link */
        padding: 0px 15px !important;
        margin: 0 !important;
        box-sizing: border-box !important;
        font-size: 14px !important;
        border-radius: 8px !important; /* Matching corners looks cleaner */
    }

    /* Fix for the WhatsApp link specifically */
    .wa-btn {
        display: inline-flex !important; /* Changed from flex to inline-flex */
        width: 100%;
        text-align: center;
    }

    /* Remove Streamlit's default widget margin which pushes buttons down */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        padding-top: 0px !important;
    }

    /* Colors */
    .claim-btn div.stButton > button { background-color: #007bff !important; color: white !important; }
    .undo-btn div.stButton > button { background-color: #6c757d !important; color: white !important; }
    .wa-btn { background-color: #25D366 !important; color: white !important; font-size: 14px; }
    
    /* Hover effects */
    .wa-btn:hover { background-color: #128C7E !important; }
</style>
""", unsafe_allow_html=True)

st.info("💡 Pro-tip: If you claim an item, please message the owner to coordinate pickup!")

# 3. Sidebar for Posting
st.sidebar.header("Post an Item")
with st.sidebar.form("post_form", clear_on_submit=True):
    name = st.text_input("Your Name")
    phone = st.text_input("WhatsApp Number (e.g., 15551234567)")
    item = st.text_input("What are you sharing? (e.g., Cherry Tomatoes)")
    category = st.selectbox("Category", ["Vegetables", "Fruit", "Cooked Meal", "Herbs", "Other"])
    qty = st.text_input("Quantity (e.g., 2 lbs, 1 plate)")
    submit = st.form_submit_button("Post to Board")

    if submit and name and item:
        df = load_data()
        new_entry = {
            "User": name, "Phone": phone, "Item": item, "Category": category, 
            "Quantity": qty, "Posted": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        st.success("Post added!")
        st.rerun()

# 4. Search & Filter Section
df = load_data()
st.divider()
search_col, cat_col = st.columns([2, 1])

with search_col:
    search_term = st.text_input("🔍 Search the board...", placeholder="e.g. Eggs, Basil")

with cat_col:
    categories = ["All", "Vegetables", "Fruit", "Cooked Meal", "Herbs", "Other"]
    selected_cat = st.selectbox("Filter by Category", categories)

# Apply Filters
if search_term:
    df = df[df['Item'].str.contains(search_term, case=False) | 
            df['User'].str.contains(search_term, case=False)]
if selected_cat != "All":
    df = df[df['Category'] == selected_cat]

# 5. Initialize Temporary Memory (Session State)
# This list resets to empty every time the app server restarts
if 'claimed_indices' not in st.session_state:
    st.session_state.claimed_indices = []


# 5. The Main Display Loop
if not df.empty:
    # Use a container to keep things tidy
    for index, row in df.iloc[::-1].iterrows():
        is_claimed = index in st.session_state.claimed_indices
        
        # Adjusting ratios: 3 parts for text, 1 for WA, 1 for Action
        cols = st.columns([3, 1, 1], vertical_alignment="center")
        
        with cols[0]:
            if is_claimed:
                st.markdown(f"### ~~{row['Item']}~~")
                st.caption("🚩 Temporarily Reserved")
            else:
                st.markdown(f"### {row['Item']}")
                st.write(f"**Owner:** {row['User']} | **Qty:** {row['Quantity']}")

        with cols[1]:
            # Use a div to help with alignment consistency
            wa_link = f"https://wa.me/{row['Phone']}?text=Hi%20{row['User']},%20is%20the%20{row['Item']}%20still%20available?"
            st.markdown(f'<a href="{wa_link}" target="_blank" class="wa-btn">💬 WhatsApp</a>', unsafe_allow_html=True)

        with cols[2]:
            if is_claimed:
                st.markdown('<div class="undo-btn">', unsafe_allow_html=True)
                if st.button("Undo ↩️", key=f"undo_{index}"):
                    st.session_state.claimed_indices.remove(index)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="claim-btn">', unsafe_allow_html=True)
                if st.button("Claim", key=f"claim_{index}_{row.get('Item', index)}"):
                    st.session_state.claimed_indices.append(index)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        st.divider()