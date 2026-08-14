import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="RAI Factory - Stock Management Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 RAI Factory — Raw Material Stock Dashboard")
st.markdown("Interactive stock tracking system for **Ayka Stock Inventory**.")

# -----------------------------------------------------------------------------
# Data Loader Function
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_parse_data(file_path):
    df_raw = pd.read_excel(file_path, sheet_name='Stock Report ', header=None)

    # 1. Paper Roll Inventory
    paper_roll = df_raw.iloc[5:30, [1, 2, 3]].dropna(how='all')
    paper_roll.columns = ['Material', 'Size / GSM', 'Qty (Rolls)']
    paper_roll = paper_roll[paper_roll['Material'] != 'Material'].dropna(subset=['Material'])
    paper_roll['Qty (Rolls)'] = pd.to_numeric(paper_roll['Qty (Rolls)'], errors='coerce').fillna(0)

    # 2. Poly Inventory
    poly_inv = df_raw.iloc[5:30, [6, 7, 8]].dropna(how='all')
    poly_inv.columns = ['Material', 'Size / Specification', 'Qty (Rolls)']
    poly_inv = poly_inv[poly_inv['Material'] != 'Material'].dropna(subset=['Material'])
    poly_inv['Qty (Rolls)'] = pd.to_numeric(poly_inv['Qty (Rolls)'], errors='coerce').fillna(0)

    # 3. Ink Stock (Normal)
    ink_normal = df_raw.iloc[5:18, [11, 12, 13]].dropna(how='all')
    ink_normal.columns = ['Colour', 'CODE', 'Qty (grams)']
    ink_normal = ink_normal[ink_normal['Colour'] != 'Colour'].dropna(subset=['Colour'])
    ink_normal['Qty (grams)'] = pd.to_numeric(ink_normal['Qty (grams)'], errors='coerce').fillna(0)

    # 4. Paper Sheet Inventory
    paper_sheet = df_raw.iloc[34:42, [1, 2, 3]].dropna(how='all')
    paper_sheet.columns = ['Material', 'Size', 'Qty (sheets)']
    paper_sheet = paper_sheet[paper_sheet['Material'] != 'Material'].dropna(subset=['Material'])
    paper_sheet['Qty (sheets)'] = pd.to_numeric(paper_sheet['Qty (sheets)'], errors='coerce').fillna(0)

    # 5. Corrugated Boxes
    boxes = df_raw.iloc[34:49, [6, 7, 8]].dropna(how='all')
    boxes.columns = ['Box Type & Specifications', 'Unit', 'Stock Qty']
    boxes = boxes[boxes['Unit'] != 'unit'].dropna(subset=['Box Type & Specifications'])
    boxes['Stock Qty'] = pd.to_numeric(boxes['Stock Qty'], errors='coerce').fillna(0)

    # 6. Cores Inventory
    cores = df_raw.iloc[34:47, [11, 12, 13]].dropna(how='all')
    cores.columns = ['Core Specifications', 'Qty', 'Unit']
    cores = cores[cores['Unit'] != 'Unit'].dropna(subset=['Core Specifications'])
    cores['Qty'] = pd.to_numeric(cores['Qty'], errors='coerce').fillna(0)

    # 7. Change Indicator Ink Stock
    indicator_ink = df_raw.iloc[52:67, [1, 2, 3, 4, 5, 10]].dropna(how='all')
    indicator_ink.columns = ['Company', 'Product Description', 'Product Code', 'Color Transition', 'Quantity (grams)', 'Remarks']
    indicator_ink = indicator_ink[indicator_ink['Company'] != 'Company'].dropna(subset=['Company'])
    indicator_ink['Quantity (grams)'] = pd.to_numeric(indicator_ink['Quantity (grams)'], errors='coerce').fillna(0)

    return {
        "Paper Roll Inventory": paper_roll,
        "Poly Inventory": poly_inv,
        "Ink Stock (Normal)": ink_normal,
        "Paper Sheet Inventory": paper_sheet,
        "Corrugated Boxes": boxes,
        "Core Inventory": cores,
        "Indicator Inks": indicator_ink
    }

# File name
EXCEL_FILE = 'Ayka stock (3).xlsx'

try:
    stock_data = load_and_parse_data(EXCEL_FILE)
except Exception as e:
    st.error(f"Error loading excel file '{EXCEL_FILE}': {e}")
    st.stop()

# -----------------------------------------------------------------------------
# KPI Metrics Bar
# -----------------------------------------------------------------------------
st.subheader("📊 Stock Overview Summary")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Paper Rolls", int(stock_data["Paper Roll Inventory"]["Qty (Rolls)"].sum()))
col2.metric("Poly Rolls", int(stock_data["Poly Inventory"]["Qty (Rolls)"].sum()))
col3.metric("Normal Ink (g)", f"{int(stock_data['Ink Stock (Normal)']['Qty (grams)'].sum()):,} g")
col4.metric("Indicator Ink (g)", f"{int(stock_data['Indicator Inks']['Quantity (grams)'].sum()):,} g")
col5.metric("Boxes Stock", int(stock_data["Corrugated Boxes"]["Stock Qty"].sum()))

st.markdown("---")

# -----------------------------------------------------------------------------
# Sidebar Navigation & Filtering
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 Inventory Navigation")
category = st.sidebar.selectbox(
    "Select Category",
    list(stock_data.keys())
)

search_term = st.sidebar.text_input("Search Item Name / Code")

# -----------------------------------------------------------------------------
# Main Section Display
# -----------------------------------------------------------------------------
st.header(f"📌 {category}")
df_category = stock_data[category].copy()

# Search Filter
if search_term:
    mask = df_category.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
    df_category = df_category[mask]

# Low Stock Alert Highlight
low_stock_threshold = st.sidebar.slider("Low Stock Alert Threshold", min_value=0, max_value=50, value=5)
st.sidebar.info(f"Highlighting items with quantity ≤ {low_stock_threshold}")

# Display Table
st.dataframe(df_category, use_container_width=True)

# -----------------------------------------------------------------------------
# Visualization Section
# -----------------------------------------------------------------------------
st.subheader("📈 Visualization")

if category in ["Paper Roll Inventory", "Poly Inventory"]:
    fig = px.bar(
        df_category,
        x="Material",
        y="Qty (Rolls)",
        color="Material",
        title=f"{category} Stock Quantity",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

elif category == "Ink Stock (Normal)":
    fig = px.pie(
        df_category,
        names="Colour",
        values="Qty (grams)",
        title="Normal Ink Distribution (grams)"
    )
    st.plotly_chart(fig, use_container_width=True)

elif category == "Corrugated Boxes":
    fig = px.bar(
        df_category,
        x="Box Type & Specifications",
        y="Stock Qty",
        title="Corrugated Boxes Stock Quantity",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

elif category == "Indicator Inks":
    fig = px.bar(
        df_category,
        x="Product Description",
        y="Quantity (grams)",
        color="Company",
        title="Indicator Ink Stock Quantity (grams)",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

# Download CSV Feature
csv_data = df_category.to_csv(index=False).encode('utf-8')
st.download_button(
    label=f"📥 Export {category} as CSV",
    data=csv_data,
    file_name=f"{category.lower().replace(' ', '_')}.csv",
    mime='text/csv'
)
