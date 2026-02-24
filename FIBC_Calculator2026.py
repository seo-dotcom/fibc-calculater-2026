import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="FIBC Sales Pro", layout="wide")

st.title("🏗️ FIBC Smart Quote & Lead System")
st.write("Professional Pricing for Feb 2026")

# --- SIDEBAR: SALES CONTROLS ---
with st.sidebar:
    st.header("Sales Dashboard")
    pp_rate = st.number_input("Current PP Rate (₹/kg)", value=102.0)
    markup = st.slider("Profit Margin %", 5, 40, 15)
    tax_rate = 18  # GST 18%
    
    st.divider()
    st.info("💡 Sales Tip: Mention that PP rates are currently stable but supply is tightening.")

# --- MAIN INTERFACE ---
col_calc, col_lead = st.columns([2, 1])

with col_calc:
    st.subheader("1. Configure Bag")
    c1, c2 = st.columns(2)
    with c1:
        l = st.number_input("Length (cm)", value=90)
        w = st.number_input("Width (cm)", value=90)
        h = st.number_input("Height (cm)", value=120)
    with c2:
        gsm = st.selectbox("Fabric GSM", [160, 170, 180, 200, 220], index=2)
        qty = st.number_input("Order Quantity", value=500, step=100)

    # Logic
    surface_area = (2 * (l/100 * h/100)) + (2 * (w/100 * h/100)) + (l/100 * w/100)
    bag_weight = (surface_area * gsm / 1000) * 1.2 # +20% for loops
    base_cost = bag_weight * pp_rate
    final_price = base_cost * (1 + (markup/100))
    total_order = final_price * qty

    # Display Results
    st.success(f"### Price per Bag: ₹{final_price:.2f}")
    st.write(f"**Total Order Value:** ₹{total_order:,.2f} + {tax_rate}% GST")

with col_lead:
    st.subheader("2. Capture Lead")
    with st.form("lead_form", clear_on_submit=True):
        client_name = st.text_input("Customer Name")
        company = st.text_input("Company Name")
        contact = st.text_input("WhatsApp / Phone")
        
        submitted = st.form_submit_button("Generate Official Quote")
        
        if submitted:
            # Here you would typically save to a database or Google Sheet
            st.balloons()
            st.write(f"✅ Lead saved for {company}!")
            st.info("Quote sent to Sales Dashboard")

# --- DATA TABLE FOR SALES ---
st.divider()
st.subheader("Order Summary")
summary_data = {
    "Specification": ["Dimensions", "GSM", "Weight", "Base Cost", "Final Price"],
    "Details": [f"{l}x{w}x{h} cm", f"{gsm} GSM", f"{bag_weight:.2f} kg", f"₹{base_cost:.2f}", f"₹{final_price:.2f}"]
}
st.table(pd.DataFrame(summary_data))