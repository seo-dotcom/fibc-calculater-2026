import streamlit as st
import pandas as pd
import datetime

# ------------------ APP CONFIG ------------------
st.set_page_config(page_title="FIBC Sales Pro", layout="wide")

st.title("🏗️ FIBC Smart Quote & Lead System")
st.write("Professional Pricing Engine – 2026")

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("Sales Dashboard")
    pp_rate = st.number_input("Current PP Rate (₹/kg)", value=102.0)
    markup = st.slider("Profit Margin %", 5, 40, 15)
    tax_rate = st.number_input("GST %", value=18)
    
    st.divider()
    st.info("💡 Sales Tip: Highlight bulk discount for 2000+ bags.")

# ------------------ MAIN LAYOUT ------------------
col_calc, col_lead = st.columns([2, 1])

# ==================================================
# CALCULATOR SECTION
# ==================================================
with col_calc:
    st.subheader("1️⃣ Configure Bag")

    c1, c2 = st.columns(2)

    with c1:
        l = st.number_input("Length (cm)", value=90)
        w = st.number_input("Width (cm)", value=90)
        h = st.number_input("Height (cm)", value=120)

    with c2:
        gsm = st.selectbox("Fabric GSM", [160, 170, 180, 200, 220], index=2)
        qty = st.number_input("Order Quantity", value=500, step=100)

    # Optional Add-ons
    st.markdown("### Add Options")
    printing = st.checkbox("Add Printing (+₹12 per bag)")
    liner = st.checkbox("Add LDPE Liner (+₹25 per bag)")

    # ------------------ CALCULATION LOGIC ------------------

    # Correct surface area (including top & bottom)
    surface_area = (2 * (l/100 * h/100)) + (2 * (w/100 * h/100)) + (2 * (l/100 * w/100))

    # Fabric weight
    fabric_weight = surface_area * gsm / 1000

    # Loop weight fixed
    loop_weight = 0.30

    bag_weight = fabric_weight + loop_weight

    base_cost = bag_weight * pp_rate

    final_price = base_cost * (1 + (markup/100))

    # Add options
    if printing:
        final_price += 12

    if liner:
        final_price += 25

    total_order = final_price * qty

    gst_amount = total_order * (tax_rate/100)
    grand_total = total_order + gst_amount

    # ------------------ DISPLAY ------------------
    st.success(f"### Price per Bag: ₹{final_price:.2f}")

    st.write(f"Subtotal: ₹{total_order:,.2f}")
    st.write(f"GST ({tax_rate}%): ₹{gst_amount:,.2f}")
    st.success(f"Grand Total: ₹{grand_total:,.2f}")

# ==================================================
# LEAD CAPTURE SECTION
# ==================================================
with col_lead:
    st.subheader("2️⃣ Capture Lead")

    with st.form("lead_form", clear_on_submit=True):
        client_name = st.text_input("Customer Name")
        company = st.text_input("Company Name")
        contact = st.text_input("WhatsApp / Phone")
        
        submitted = st.form_submit_button("Generate Official Quote")
        
        if submitted:
            # Save lead to CSV
            new_lead = pd.DataFrame({
                "Date": [datetime.datetime.now()],
                "Client": [client_name],
                "Company": [company],
                "Contact": [contact],
                "Dimensions": [f"{l}x{w}x{h} cm"],
                "GSM": [gsm],
                "Price per Bag": [final_price],
                "Quantity": [qty],
                "Total Order": [grand_total]
            })

            new_lead.to_csv("leads.csv", mode='a', header=False, index=False)

            st.balloons()
            st.success("✅ Lead Saved Successfully!")

            # Generate Quotation Text
            quotation = f"""
FIBC QUOTATION

Customer: {client_name}
Company: {company}

Bag Specification:
Dimensions: {l}x{w}x{h} cm
Fabric GSM: {gsm}
Printing: {'Yes' if printing else 'No'}
Liner: {'Yes' if liner else 'No'}

Price per Bag: ₹{final_price:.2f}
Quantity: {qty}
Subtotal: ₹{total_order:,.2f}
GST ({tax_rate}%): ₹{gst_amount:,.2f}

Grand Total: ₹{grand_total:,.2f}

Thank you for your business.
"""

            st.download_button(
                label="📄 Download Quotation",
                data=quotation,
                file_name="FIBC_Quotation.txt",
                mime="text/plain"
            )

# ==================================================
# ORDER SUMMARY TABLE
# ==================================================
st.divider()
st.subheader("📊 Order Summary")

summary_data = {
    "Specification": [
        "Dimensions",
        "GSM",
        "Fabric Weight (kg)",
        "Loop Weight (kg)",
        "Base Cost",
        "Final Price per Bag"
    ],
    "Details": [
        f"{l}x{w}x{h} cm",
        f"{gsm} GSM",
        f"{fabric_weight:.2f}",
        f"{loop_weight:.2f}",
        f"₹{base_cost:.2f}",
        f"₹{final_price:.2f}"
    ]
}

st.table(pd.DataFrame(summary_data))
