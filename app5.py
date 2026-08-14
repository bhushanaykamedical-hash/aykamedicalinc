import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Rai Factory - Complete Stock Management",
    layout="wide",
    page_icon="📦"
)

# ---------------------------------------------------------
# DATABASE SETUP & INITIALIZATION
# ---------------------------------------------------------
DB_NAME = "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Paper Roll Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_roll_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            size_gsm TEXT NOT NULL,
            qty_rolls INTEGER DEFAULT 0
        )
    """)

    # 2. Poly Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS poly_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            size_spec TEXT NOT NULL,
            qty_rolls INTEGER DEFAULT 0
        )
    """)

    # 3. Ink Stock (Normal) Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ink_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colour TEXT NOT NULL,
            code TEXT,
            qty_grams REAL DEFAULT 0.0
        )
    """)

    # 4. Paper Sheet Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_sheet_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            size TEXT NOT NULL,
            qty_sheets INTEGER DEFAULT 0
        )
    """)

    # 5a. Corrugated Boxes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS box_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_spec TEXT NOT NULL,
            unit TEXT DEFAULT 'Pcs',
            stock_qty INTEGER DEFAULT 0
        )
    """)

    # 5b. Core Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            core_spec TEXT NOT NULL,
            qty INTEGER DEFAULT 0,
            unit TEXT DEFAULT 'Pcs'
        )
    """)

    # 6. Indicator Colour Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicator_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            description TEXT,
            code TEXT,
            color_transition TEXT,
            qty_grams REAL DEFAULT 0.0,
            remarks TEXT
        )
    """)

    # --- Seed Data 1: Paper Roll Inventory ---
    cursor.execute("SELECT COUNT(*) FROM paper_roll_inventory")
    if cursor.fetchone()[0] == 0:
        paper_roll_initial = [
            ("Medi-Craft", "410×3000 mtr (60 GSM)", 4),
            ("Medi-Craft", "610×3000 mtr (60 GSM)", 18),
            ("Medi-Craft", "610×2000 mtr (60 GSM)", 0),
            ("Medi-Craft", "930×2000 mtr (60 GSM)", 1),
            ("Medi-Craft", "420×2000 mtr (60 GSM)", 0),
            ("Pelta Med", "610×3500 mtr (62 GSM)", 49),
            ("Pelta Med", "410×3500 mtr (62 GSM)", 32),
            ("Pelta Med", "930×3500 mtr (62 GSM)", 5),
            ("Pelta Med", "570×3500 mtr (62 GSM)", 8),
            ("Pelta Med", "930×3500 mtr (68 GSM)", 11),
            ("Pelta Med", "610×2400 mtr (68 GSM)", 11),
            ("Shivshakti Piggybag", "200×700 mtr (300gsm)", 2),
            ("Shivshakti Piggybag", "200×1000 mtr (300gsm)", 20),
            ("Avory Roll", "100×680 mtr (300gsm)", 11),
            ("Avory Roll", "200×680 mtr (300gsm)", 0),
            ("Avory Roll", "300×1000 mtr (300gsm)", 2),
            ("Filter Face Mask", "175×2000 mtr", 38),
            ("White Mask Roll", "175×2000 mtr", 23),
            ("Blue Mask Roll", "190×2000 mtr", 12),
            ("Elastic Roll", "190 (90gsm)", 8),
            ("Tyvek Roll", "1100×1000 mtr", 0),
            ("Autoclave ROLL", "912×1000 mtr", 0),
            ("ETO ROLL", "912×1000 mtr", 0),
            ("Tyvek Roll", "1100x1035mtr (60gsm)", 1),
        ]
        cursor.executemany(
            "INSERT INTO paper_roll_inventory (material, size_gsm, qty_rolls) VALUES (?, ?, ?)",
            paper_roll_initial,
        )

    # --- Seed Data 2: Poly Inventory ---
    cursor.execute("SELECT COUNT(*) FROM poly_inventory")
    if cursor.fetchone()[0] == 0:
        poly_initial = [
            ("Blue Film (46micron)", "410×2500 mtr", 14),
            ("Blue Film (46micron)", "410×1200 mtr", 4),
            ("Blue Film (46micron)", "410×1600 mtr", 1),
            ("Blue Film (46micron)", "410×1500 mtr", 1),
            ("Blue Film (46micron)", "310×2100 mtr", 3),
            ("Blue Film (46micron)", "360×2100 mtr", 11),
            ("Blue Film (46micron)", "510×2000 mtr", 7),
            ("Blue Film (46micron)", "510×1700 mtr", 2),
            ("Blue Film (46micron)", "510×1550 mtr", 16),
            ("Blue Film (46micron)", "610×1350 mtr", 37),
            ("Blue Film (46micron)", "930×1600 mtr", 5),
            ("Blue Film (46micron)", "930×1370 mtr", 1),
            ("Blue Film (46micron)", "930×790 mtr", 1),
            ("Tyvek Film", "930×2200 mtr", 1),
            ("White Film (46micron)", "570×1750 mtr", 6),
            ("White Film (46micron)", "570×1600 mtr", 2),
            ("White Film (46micron)", "570×1950 mtr", 2),
            ("White Film (46micron)", "410×2080 mtr", 13),
            ("White Film (62micron)", "410×1285 mtr", 6),
            ("White Film (62micron)", "510×1285 mtr", 7),
            ("White Film (46micron)", "610×1480 mtr", 12),
            ("White Film (46micron)", "1000×1700 mtr", 6),
            ("Tyvek Film", "840×3000 mtr", 0),
        ]
        cursor.executemany(
            "INSERT INTO poly_inventory (material, size_spec, qty_rolls) VALUES (?, ?, ?)",
            poly_initial,
        )

    # --- Seed Data 3: Ink Stock (Normal) ---
    cursor.execute("SELECT COUNT(*) FROM ink_inventory")
    if cursor.fetchone()[0] == 0:
        ink_initial = [
            ("Purple", "5133", 7300.0),
            ("Dark Blue", "10610", 3800.0),
            ("Blue", "2640", 5200.0),
            ("Blue", "0", 5000.0),
            ("Metallic Blue", "2325", 3570.0),
            ("Sky Blue", "10611", 3780.0),
            ("Black", "0", 1500.0),
            ("TEST Medium", "0", 5100.0),
            ("Violet blue", "8667", 5700.0),
            ("Green", "2819", 4970.0),
            ("Magenta", "10522", 4850.0),
            ("Lemon Yellow", "10521", 16520.0),
        ]
        cursor.executemany(
            "INSERT INTO ink_inventory (colour, code, qty_grams) VALUES (?, ?, ?)",
            ink_initial,
        )

    # --- Seed Data 4: Paper Sheet Inventory ---
    cursor.execute("SELECT COUNT(*) FROM paper_sheet_inventory")
    if cursor.fetchone()[0] == 0:
        sheet_initial = [
            ("SHIV SHAKTI Gumming Paper", "13inch×19inch", 10512),
            ("SHIV SHAKTI Paper plain ( Bowie Dick)", "13inch×19inch", 1263),
            ("BOWIE DICK A4 Paper", "210mm×297mm", 1697),
            ("BOWIE DICK Lot Sheet", "114mm×125mm", 1092500),
            ("BOWIE DICK Card Sheet", "114mm×125mm", 5775),
            ("Green Paper", "12inch×12inch", 1000),
            ("Acrylic Paper", "12inch×18inch", 160),
        ]
        cursor.executemany(
            "INSERT INTO paper_sheet_inventory (material, size, qty_sheets) VALUES (?, ?, ?)",
            sheet_initial,
        )

    # --- Seed Data 5a: Corrugated Boxes ---
    cursor.execute("SELECT COUNT(*) FROM box_inventory")
    if cursor.fetchone()[0] == 0:
        box_initial = [
            ("Ayka Small Printed Reel corrugated Box (44*23*32)", "Pcs", 654),
            ("Ayka Large Printed Reel corrugated box (44*23*42)", "Pcs", 420),
            ("Ayka Large printed wrap box (44*23*42)", "Pcs", 0),
            ("Bowie Dick Inner box (30*12.5)", "Pcs", 6863),
            ("Bowie Dick Outer Box (15.5*11.8)", "Pcs", 9490),
            ("Plain Bowie Dick corrugated Box (26*24*14)", "Pcs", 500),
            ("Plain Master Carton Box for face mask (50*20*50)", "Pcs", 10),
            ("Plain small Pouch box (34*23*29)", "Pcs", 405),
            ("Plain small Autoclave/Label box (28*26*28)", "Pcs", 370),
            ("Plain small Reel box (44*23*32)", "Pcs", 524),
            ("Indicator Master Carton Box (21*18*11.5)", "Pcs", 600),
            ("Plain master carton box bowie dick-longline (55*17.5.17)", "Pcs", 100),
            ("Plain Large Reel box (44*23*42)", "Pcs", 220),
            ("Plain master caton box (23*23*53/Reel size-500)", "Pcs", 100),
        ]
        cursor.executemany(
            "INSERT INTO box_inventory (box_spec, unit, stock_qty) VALUES (?, ?, ?)",
            box_initial,
        )

    # --- Seed Data 5b: Core Specifications ---
    cursor.execute("SELECT COUNT(*) FROM core_inventory")
    if cursor.fetchone()[0] == 0:
        core_initial = [
            ("Cardboard Core (55mm)", 450, "Pcs"),
            ("Cardboard Core (75mm)", 165, "Pcs"),
            ("Cardboard Core (100mm)", 906, "Pcs"),
            ("Cardboard Core (125mm)", 154, "Pcs"),
            ("Cardboard Core (150mm)", 1270, "Pcs"),
            ("Cardboard Core (200mm)", 826, "Pcs"),
            ("Cardboard Core (250mm)", 670, "Pcs"),
            ("Cardboard Core (300mm)", 36, "Pcs"),
            ("Cardboard Core (350mm)", 277, "Pcs"),
            ("Cardboard Core (400mm)", 461, "Pcs"),
            ("Cardboard Core (500mm)", 190, "Pcs"),
            ("Core Plastic (32mm)", 82280, "Pcs"),
        ]
        cursor.executemany(
            "INSERT INTO core_inventory (core_spec, qty, unit) VALUES (?, ?, ?)",
            core_initial,
        )

    # --- Seed Data 6: Indicator Colour Inventory ---
    cursor.execute("SELECT COUNT(*) FROM indicator_inventory")
    if cursor.fetchone()[0] == 0:
        indicator_initial = [
            ("Chroma Inks", "ETO - Yellow", "CL/FYC/EO/4", "Yellow to brown", 4734.0, "LABEL"),
            ("Chroma Inks", "ETO - Pink", "CL/FRC/EO/2", "Pink To Brown", 7180.0, "REEL"),
            ("Chroma Inks", "Plasma - Red", "CL/FRY/PLA/2", "Red", 1260.0, "TYVEK REEL"),
            ("Tempil Ink", "Steam - Green", "TISFRG1010GL-27566", "Green", 700.0, "LABEL"),
            ("Tempil Ink", "Steam - Green", "TIS784-B/858.ACT/GL-27505", "Green", 13900.0, "LABEL"),
            ("Tempil Ink", "Steam - Blue", "TISFAC858.1GL-27518", "Blue", 8700.0, "INDICATOR"),
            ("Tempil Ink", "Steam - Blue", "TISFAC663-GL-27510", "Blue", 1200.0, "REEL"),
            ("Tempil Ink", "Steam - Pink", "TISFRC784B.2GL-27539", "Pink", 4930.0, "INDICATOR/BD TEST Sheet"),
            ("OTS", "Plasma - Blue", "VH2O2-BR", "Blue to red", 990.0, "INDICATOR (TRIAL)"),
            ("OTS", "Steam - PB", "STEAM-PB", "Purple to Green", 8500.0, "LABEL"),
            ("OTS", "Plasma - Red", "VH2O2-RY", "Red To Yellow", 7700.0, "INDICATOR"),
            ("OTS", "ETO - Yellow", "EO-YB", "Yellow to brown", 5500.0, "LABEL"),
            ("OTS", "Formaldehyde - Red", "HCHO-RG", "Red to Green", 5200.0, ""),
            ("OTS", "China Pink", "STEAM-RB", "----------", 0.0, ""),
        ]
        cursor.executemany(
            "INSERT INTO indicator_inventory (company, description, code, color_transition, qty_grams, remarks) VALUES (?, ?, ?, ?, ?, ?)",
            indicator_initial,
        )

    conn.commit()
    conn.close()


# Initialize database tables & seed data
init_db()

# ---------------------------------------------------------
# APP INTERFACE
# ---------------------------------------------------------
st.title("🏭 Rai Factory - RAW MATERIAL STOCK MANAGEMENT")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "1. Paper Roll Inventory",
        "2. Poly Inventory",
        "3. Ink Stock (Normal)",
        "4. Paper Sheet Inventory",
        "5. Boxes & Cores",
        "6. Indicator Colour",
        "⚡ Stock Transactions",
    ]
)

# --- TAB 1: PAPER ROLL INVENTORY ---
with tab1:
    st.subheader("1. Paper Roll Inventory")
    search = st.text_input("🔍 Search Material / Size:", key="search_paper_roll")
    conn = get_db_connection()
    if search:
        df = pd.read_sql_query(
            "SELECT material AS 'Material', size_gsm AS 'Size / GSM', qty_rolls AS 'Qty (Rolls)' FROM paper_roll_inventory WHERE material LIKE ? OR size_gsm LIKE ?",
            conn, params=(f"%{search}%", f"%{search}%")
        )
    else:
        df = pd.read_sql_query("SELECT material AS 'Material', size_gsm AS 'Size / GSM', qty_rolls AS 'Qty (Rolls)' FROM paper_roll_inventory", conn)
    conn.close()

    st.dataframe(df)
    st.metric("Total Paper Rolls", int(df["Qty (Rolls)"].sum() if not df.empty else 0))

# --- TAB 2: POLY INVENTORY ---
with tab2:
    st.subheader("2. Poly Inventory Stock")
    search = st.text_input("🔍 Search Material / Specification:", key="search_poly")
    conn = get_db_connection()
    if search:
        df = pd.read_sql_query(
            "SELECT material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory WHERE material LIKE ? OR size_spec LIKE ?",
            conn, params=(f"%{search}%", f"%{search}%")
        )
    else:
        df = pd.read_sql_query("SELECT material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory", conn)
    conn.close()

    st.dataframe(df)
    st.metric("Total Poly Rolls", int(df["Qty (Rolls)"].sum() if not df.empty else 0))

# --- TAB 3: INK STOCK (NORMAL) ---
with tab3:
    st.subheader("3. Ink Stock (Normal)")
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT colour AS 'Colour', code AS 'CODE', qty_grams AS 'Qty (grams)' FROM ink_inventory", conn)
    conn.close()

    st.dataframe(df)
    total_g = df["Qty (grams)"].sum() if not df.empty else 0
    st.metric("Total Ink Weight (Grams)", f"{total_g:,.0f} g")

# --- TAB 4: PAPER SHEET INVENTORY ---
with tab4:
    st.subheader("4. Paper Sheet Inventory")
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT material AS 'Material', size AS 'Size', qty_sheets AS 'Qty (sheets)' FROM paper_sheet_inventory", conn)
    conn.close()

    st.dataframe(df)
    st.metric("Total Paper Sheets", f"{int(df['Qty (sheets)'].sum() if not df.empty else 0):,}")

# --- TAB 5: CORRUGATED BOXES & CORE INVENTORY ---
with tab5:
    col1, col2 = st.columns(2)
    conn = get_db_connection()
    df_box = pd.read_sql_query("SELECT box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory", conn)
    df_core = pd.read_sql_query("SELECT core_spec AS 'Core Specifications', qty AS 'Qty', unit AS 'Unit' FROM core_inventory", conn)
    conn.close()

    with col1:
        st.subheader("Corrugated Boxes")
        st.dataframe(df_box)
        st.metric("Total Boxes (Pcs)", f"{int(df_box['Stock Qty'].sum() if not df_box.empty else 0):,}")

    with col2:
        st.subheader("Core Specifications")
        st.dataframe(df_core)
        st.metric("Total Cores (Pcs)", f"{int(df_core['Qty'].sum() if not df_core.empty else 0):,}")

# --- TAB 6: INDICATOR COLOUR ---
with tab6:
    st.subheader("6. Change Indicator Colour Inventory")
    conn = get_db_connection()
    df = pd.read_sql_query(
        "SELECT company AS 'Company', description AS 'Product Description', code AS 'Product Code', color_transition AS 'Color Transition', qty_grams AS 'Quantity (grams)', remarks AS 'REMARKS' FROM indicator_inventory",
        conn
    )
    conn.close()

    st.dataframe(df)
    total_ind_g = df["Quantity (grams)"].sum() if not df.empty else 0
    c1, c2 = st.columns(2)
    c1.metric("Total Weight (Grams)", f"{total_ind_g:,.0f} g")
    c2.metric("Total Weight (KG)", f"{total_ind_g / 1000:,.2f} kg")

# --- TAB 7: TRANSACTIONS (IN/OUT UPDATES) ---
with tab7:
    st.subheader("⚡ Update Inventory Quantities (Stock IN / Stock OUT)")
    
    category = st.selectbox(
        "Select Section to Update:",
        [
            "1. Paper Roll Inventory",
            "2. Poly Inventory",
            "3. Ink Stock (Normal)",
            "4. Paper Sheet Inventory",
            "5. Corrugated Boxes",
            "6. Core Specifications",
            "7. Indicator Colour",
        ],
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    if category == "1. Paper Roll Inventory":
        items = pd.read_sql_query("SELECT id, material || ' | ' || size_gsm AS label FROM paper_roll_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Paper Roll Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Rolls Quantity", min_value=1, step=1)

            if st.button("Update Paper Roll Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE paper_roll_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Paper Roll Stock updated successfully!")
                st.rerun()

    elif category == "2. Poly Inventory":
        items = pd.read_sql_query("SELECT id, material || ' | ' || size_spec AS label FROM poly_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Poly Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Rolls Quantity", min_value=1, step=1)

            if st.button("Update Poly Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE poly_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Poly Stock updated successfully!")
                st.rerun()

    elif category == "3. Ink Stock (Normal)":
        items = pd.read_sql_query("SELECT id, colour || ' (Code: ' || code || ')' AS label FROM ink_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Ink", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Grams Quantity", min_value=1.0, step=100.0)

            if st.button("Update Ink Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE ink_inventory SET qty_grams = MAX(0, qty_grams {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Ink Stock updated successfully!")
                st.rerun()

    elif category == "4. Paper Sheet Inventory":
        items = pd.read_sql_query("SELECT id, material || ' (' || size || ')' AS label FROM paper_sheet_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Sheet Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Sheet Quantity", min_value=1, step=100)

            if st.button("Update Sheet Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE paper_sheet_inventory SET qty_sheets = MAX(0, qty_sheets {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Paper Sheet Stock updated successfully!")
                st.rerun()

    elif category == "5. Corrugated Boxes":
        items = pd.read_sql_query("SELECT id, box_spec FROM box_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Box Item", items["box_spec"])
            selected_id = int(items[items["box_spec"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Box Quantity (Pcs)", min_value=1, step=10)

            if st.button("Update Box Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE box_inventory SET stock_qty = MAX(0, stock_qty {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Box Stock updated successfully!")
                st.rerun()

    elif category == "6. Core Specifications":
        items = pd.read_sql_query("SELECT id, core_spec FROM core_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Core Specification", items["core_spec"])
            selected_id = int(items[items["core_spec"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Core Quantity (Pcs)", min_value=1, step=10)

            if st.button("Update Core Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE core_inventory SET qty = MAX(0, qty {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Core Stock updated successfully!")
                st.rerun()

    elif category == "7. Indicator Colour":
        items = pd.read_sql_query("SELECT id, company || ' | ' || description || ' (' || code || ')' AS label FROM indicator_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Indicator Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Grams Quantity", min_value=1.0, step=100.0)

            if st.button("Update Indicator Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE indicator_inventory SET qty_grams = MAX(0, qty_grams {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Indicator Colour Stock updated successfully!")
                st.rerun()

    conn.close()    # 2. Poly Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS poly_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            size_spec TEXT NOT NULL,
            qty_rolls INTEGER DEFAULT 0
        )
    """)

    # 3. Ink Stock (Normal) Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ink_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colour TEXT NOT NULL,
            code TEXT,
            qty_grams REAL DEFAULT 0.0
        )
    """)

    # 4. Paper Sheet Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_sheet_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            size TEXT NOT NULL,
            qty_sheets INTEGER DEFAULT 0
        )
    """)

    # 5a. Corrugated Boxes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS box_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_spec TEXT NOT NULL,
            unit TEXT DEFAULT 'Pcs',
            stock_qty INTEGER DEFAULT 0
        )
    """)

    # 5b. Core Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS core_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            core_spec TEXT NOT NULL,
            qty INTEGER DEFAULT 0,
            unit TEXT DEFAULT 'Pcs'
        )
    """)

    # 6. Indicator Colour Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicator_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            description TEXT,
            code TEXT,
            color_transition TEXT,
            qty_grams REAL DEFAULT 0.0,
            remarks TEXT
        )
    """)

    # --- Seed Data 1: Paper Roll Inventory ---
    cursor.execute("SELECT COUNT(*) FROM paper_roll_inventory")
    if cursor.fetchone()[0] == 0:
        paper_roll_initial = [
            ("Medi-Craft", "410×3000 mtr (60 GSM)", 4),
            ("Medi-Craft", "610×3000 mtr (60 GSM)", 18),
            ("Medi-Craft", "610×2000 mtr (60 GSM)", 0),
            ("Medi-Craft", "930×2000 mtr (60 GSM)", 1),
            ("Medi-Craft", "420×2000 mtr (60 GSM)", 0),
            ("Pelta Med", "610×3500 mtr (62 GSM)", 49),
            ("Pelta Med", "410×3500 mtr (62 GSM)", 32),
            ("Pelta Med", "930×3500 mtr (62 GSM)", 5),
            ("Pelta Med", "570×3500 mtr (62 GSM)", 8),
            ("Pelta Med", "930×3500 mtr (68 GSM)", 11),
            ("Pelta Med", "610×2400 mtr (68 GSM)", 11),
            ("Shivshakti Piggybag", "200×700 mtr (300gsm)", 2),
            ("Shivshakti Piggybag", "200×1000 mtr (300gsm)", 20),
            ("Avory Roll", "100×680 mtr (300gsm)", 11),
            ("Avory Roll", "200×680 mtr (300gsm)", 0),
            ("Avory Roll", "300×1000 mtr (300gsm)", 2),
            ("Filter Face Mask", "175×2000 mtr", 38),
            ("White Mask Roll", "175×2000 mtr", 23),
            ("Blue Mask Roll", "190×2000 mtr", 12),
            ("Elastic Roll", "190 (90gsm)", 8),
            ("Tyvek Roll", "1100×1000 mtr", 0),
            ("Autoclave ROLL", "912×1000 mtr", 0),
            ("ETO ROLL", "912×1000 mtr", 0),
            ("Tyvek Roll", "1100x1035mtr (60gsm)", 1),
        ]
        cursor.executemany(
            "INSERT INTO paper_roll_inventory (material, size_gsm, qty_rolls) VALUES (?, ?, ?)",
            paper_roll_initial,
        )

    # --- Seed Data 2: Poly Inventory ---
    cursor.execute("SELECT COUNT(*) FROM poly_inventory")
    if cursor.fetchone()[0] == 0:
        poly_initial = [
            ("Blue Film (46micron)", "410×2500 mtr", 14),
            ("Blue Film (46micron)", "410×1200 mtr", 4),
            ("Blue Film (46micron)", "410×1600 mtr", 1),
            ("Blue Film (46micron)", "410×1500 mtr", 1),
            ("Blue Film (46micron)", "310×2100 mtr", 3),
            ("Blue Film (46micron)", "360×2100 mtr", 11),
            ("Blue Film (46micron)", "510×2000 mtr", 7),
            ("Blue Film (46micron)", "510×1700 mtr", 2),
            ("Blue Film (46micron)", "510×1550 mtr", 16),
            ("Blue Film (46micron)", "610×1350 mtr", 37),
            ("Blue Film (46micron)", "930×1600 mtr", 5),
            ("Blue Film (46micron)", "930×1370 mtr", 1),
            ("Blue Film (46micron)", "930×790 mtr", 1),
            ("Tyvek Film", "930×2200 mtr", 1),
            ("White Film (46micron)", "570×1750 mtr", 6),
            ("White Film (46micron)", "570×1600 mtr", 2),
            ("White Film (46micron)", "570×1950 mtr", 2),
            ("White Film (46micron)", "410×2080 mtr", 13),
            ("White Film (62micron)", "410×1285 mtr", 6),
            ("White Film (62micron)", "510×1285 mtr", 7),
            ("White Film (46micron)", "610×1480 mtr", 12),
            ("White Film (46micron)", "1000×1700 mtr", 6),
            ("Tyvek Film", "840×3000 mtr", 0),
        ]
        cursor.executemany(
            "INSERT INTO poly_inventory (material, size_spec, qty_rolls) VALUES (?, ?, ?)",
            poly_initial,
        )

    # --- Seed Data 3: Ink Stock (Normal) ---
    cursor.execute("SELECT COUNT(*) FROM ink_inventory")
    if cursor.fetchone()[0] == 0:
        ink_initial = [
            ("Purple", "5133", 7300.0),
            ("Dark Blue", "10610", 3800.0),
            ("Blue", "2640", 5200.0),
            ("Blue", "0", 5000.0),
            ("Metallic Blue", "2325", 3570.0),
            ("Sky Blue", "10611", 3780.0),
            ("Black", "0", 1500.0),
            ("TEST Medium", "0", 5100.0),
            ("Violet blue", "8667", 5700.0),
            ("Green", "2819", 4970.0),
            ("Magenta", "10522", 4850.0),
            ("Lemon Yellow", "10521", 16520.0),
        ]
        cursor.executemany(
            "INSERT INTO ink_inventory (colour, code, qty_grams) VALUES (?, ?, ?)",
            ink_initial,
        )

    # --- Seed Data 4: Paper Sheet Inventory ---
    cursor.execute("SELECT COUNT(*) FROM paper_sheet_inventory")
    if cursor.fetchone()[0] == 0:
        sheet_initial = [
            ("SHIV SHAKTI Gumming Paper", "13inch×19inch", 10512),
            ("SHIV SHAKTI Paper plain ( Bowie Dick)", "13inch×19inch", 1263),
            ("BOWIE DICK A4 Paper", "210mm×297mm", 1697),
            ("BOWIE DICK Lot Sheet", "114mm×125mm", 1092500),
            ("BOWIE DICK Card Sheet", "114mm×125mm", 5775),
            ("Green Paper", "12inch×12inch", 1000),
            ("Acrylic Paper", "12inch×18inch", 160),
        ]
        cursor.executemany(
            "INSERT INTO paper_sheet_inventory (material, size, qty_sheets) VALUES (?, ?, ?)",
            sheet_initial,
        )

    # --- Seed Data 5a: Corrugated Boxes ---
    cursor.execute("SELECT COUNT(*) FROM box_inventory")
    if cursor.fetchone()[0] == 0:
        box_initial = [
            ("Ayka Small Printed Reel corrugated Box (44*23*32)", "Pcs", 654),
            ("Ayka Large Printed Reel corrugated box (44*23*42)", "Pcs", 420),
            ("Ayka Large printed wrap box (44*23*42)", "Pcs", 0),
            ("Bowie Dick Inner box (30*12.5)", "Pcs", 6863),
            ("Bowie Dick Outer Box (15.5*11.8)", "Pcs", 9490),
            ("Plain Bowie Dick corrugated Box (26*24*14)", "Pcs", 500),
            ("Plain Master Carton Box for face mask (50*20*50)", "Pcs", 10),
            ("Plain small Pouch box (34*23*29)", "Pcs", 405),
            ("Plain small Autoclave/Label box (28*26*28)", "Pcs", 370),
            ("Plain small Reel box (44*23*32)", "Pcs", 524),
            ("Indicator Master Carton Box (21*18*11.5)", "Pcs", 600),
            ("Plain master carton box bowie dick-longline (55*17.5.17)", "Pcs", 100),
            ("Plain Large Reel box (44*23*42)", "Pcs", 220),
            ("Plain master caton box (23*23*53/Reel size-500)", "Pcs", 100),
        ]
        cursor.executemany(
            "INSERT INTO box_inventory (box_spec, unit, stock_qty) VALUES (?, ?, ?)",
            box_initial,
        )

    # --- Seed Data 5b: Core Specifications ---
    cursor.execute("SELECT COUNT(*) FROM core_inventory")
    if cursor.fetchone()[0] == 0:
        core_initial = [
            ("Cardboard Core (55mm)", 450, "Pcs"),
            ("Cardboard Core (75mm)", 165, "Pcs"),
            ("Cardboard Core (100mm)", 906, "Pcs"),
            ("Cardboard Core (125mm)", 154, "Pcs"),
            ("Cardboard Core (150mm)", 1270, "Pcs"),
            ("Cardboard Core (200mm)", 826, "Pcs"),
            ("Cardboard Core (250mm)", 670, "Pcs"),
            ("Cardboard Core (300mm)", 36, "Pcs"),
            ("Cardboard Core (350mm)", 277, "Pcs"),
            ("Cardboard Core (400mm)", 461, "Pcs"),
            ("Cardboard Core (500mm)", 190, "Pcs"),
            ("Core Plastic (32mm)", 82280, "Pcs"),
        ]
        cursor.executemany(
            "INSERT INTO core_inventory (core_spec, qty, unit) VALUES (?, ?, ?)",
            core_initial,
        )

    # --- Seed Data 6: Indicator Colour Inventory ---
    cursor.execute("SELECT COUNT(*) FROM indicator_inventory")
    if cursor.fetchone()[0] == 0:
        indicator_initial = [
            ("Chroma Inks", "ETO - Yellow", "CL/FYC/EO/4", "Yellow to brown", 4734.0, "LABEL"),
            ("Chroma Inks", "ETO - Pink", "CL/FRC/EO/2", "Pink To Brown", 7180.0, "REEL"),
            ("Chroma Inks", "Plasma - Red", "CL/FRY/PLA/2", "Red", 1260.0, "TYVEK REEL"),
            ("Tempil Ink", "Steam - Green", "TISFRG1010GL-27566", "Green", 700.0, "LABEL"),
            ("Tempil Ink", "Steam - Green", "TIS784-B/858.ACT/GL-27505", "Green", 13900.0, "LABEL"),
            ("Tempil Ink", "Steam - Blue", "TISFAC858.1GL-27518", "Blue", 8700.0, "INDICATOR"),
            ("Tempil Ink", "Steam - Blue", "TISFAC663-GL-27510", "Blue", 1200.0, "REEL"),
            ("Tempil Ink", "Steam - Pink", "TISFRC784B.2GL-27539", "Pink", 4930.0, "INDICATOR/BD TEST Sheet"),
            ("OTS", "Plasma - Blue", "VH2O2-BR", "Blue to red", 990.0, "INDICATOR (TRIAL)"),
            ("OTS", "Steam - PB", "STEAM-PB", "Purple to Green", 8500.0, "LABEL"),
            ("OTS", "Plasma - Red", "VH2O2-RY", "Red To Yellow", 7700.0, "INDICATOR"),
            ("OTS", "ETO - Yellow", "EO-YB", "Yellow to brown", 5500.0, "LABEL"),
            ("OTS", "Formaldehyde - Red", "HCHO-RG", "Red to Green", 5200.0, ""),
            ("OTS", "China Pink", "STEAM-RB", "----------", 0.0, ""),
        ]
        cursor.executemany(
            "INSERT INTO indicator_inventory (company, description, code, color_transition, qty_grams, remarks) VALUES (?, ?, ?, ?, ?, ?)",
            indicator_initial,
        )

    conn.commit()
    conn.close()


# Run DB setup
init_db()

# ---------------------------------------------------------
# APP INTERFACE
# ---------------------------------------------------------
st.title("🏭 Rai Factory - RAW MATERIAL STOCK MANAGEMENT")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "1. Paper Roll Inventory",
        "2. Poly Inventory",
        "3. Ink Stock (Normal)",
        "4. Paper Sheet Inventory",
        "5. Boxes & Cores",
        "6. Indicator Colour",
        "⚡ Stock Transactions",
    ]
)

# --- TAB 1: PAPER ROLL INVENTORY ---
with tab1:
    st.subheader("1. Paper Roll Inventory")
    search = st.text_input("🔍 Search Material / Size:", key="search_paper_roll")
    conn = get_db_connection()
    if search:
        df = pd.read_sql_query(
            "SELECT material AS 'Material', size_gsm AS 'Size / GSM', qty_rolls AS 'Qty (Rolls)' FROM paper_roll_inventory WHERE material LIKE ? OR size_gsm LIKE ?",
            conn, params=(f"%{search}%", f"%{search}%")
        )
    else:
        df = pd.read_sql_query("SELECT material AS 'Material', size_gsm AS 'Size / GSM', qty_rolls AS 'Qty (Rolls)' FROM paper_roll_inventory", conn)
    conn.close()

    st.dataframe(df)
    st.metric("Total Paper Rolls", int(df["Qty (Rolls)"].sum() if not df.empty else 0))

# --- TAB 2: POLY INVENTORY ---
with tab2:
    st.subheader("2. Poly Inventory Stock")
    search = st.text_input("🔍 Search Material / Specification:", key="search_poly")
    conn = get_db_connection()
    if search:
        df = pd.read_sql_query(
            "SELECT material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory WHERE material LIKE ? OR size_spec LIKE ?",
            conn, params=(f"%{search}%", f"%{search}%")
        )
    else:
        df = pd.read_sql_query("SELECT material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory", conn)
    conn.close()

    st.dataframe(df)
    st.metric("Total Poly Rolls", int(df["Qty (Rolls)"].sum() if not df.empty else 0))

# --- TAB 3: INK STOCK (NORMAL) ---
with tab3:
    st.subheader("3. Ink Stock (Normal)")
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT colour AS 'Colour', code AS 'CODE', qty_grams AS 'Qty (grams)' FROM ink_inventory", conn)
    conn.close()

    st.dataframe(df)
    total_g = df["Qty (grams)"].sum() if not df.empty else 0
    st.metric("Total Ink Weight (Grams)", f"{total_g:,.0f} g")

# --- TAB 4: PAPER SHEET INVENTORY ---
with tab4:
    st.subheader("4. Paper Sheet Inventory")
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT material AS 'Material', size AS 'Size', qty_sheets AS 'Qty (sheets)' FROM paper_sheet_inventory", conn)
    conn.close()

    st.dataframe(df)
    st.metric("Total Paper Sheets", f"{int(df['Qty (sheets)'].sum() if not df.empty else 0):,}")

# --- TAB 5: CORRUGATED BOXES & CORE INVENTORY ---
with tab5:
    col1, col2 = st.columns(2)
    conn = get_db_connection()
    df_box = pd.read_sql_query("SELECT box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory", conn)
    df_core = pd.read_sql_query("SELECT core_spec AS 'Core Specifications', qty AS 'Qty', unit AS 'Unit' FROM core_inventory", conn)
    conn.close()

    with col1:
        st.subheader("Corrugated Boxes")
        st.dataframe(df_box)
        st.metric("Total Boxes (Pcs)", f"{int(df_box['Stock Qty'].sum() if not df_box.empty else 0):,}")

    with col2:
        st.subheader("Core Specifications")
        st.dataframe(df_core)
        st.metric("Total Cores (Pcs)", f"{int(df_core['Qty'].sum() if not df_core.empty else 0):,}")

# --- TAB 6: INDICATOR COLOUR ---
with tab6:
    st.subheader("6. Change Indicator Colour Inventory")
    conn = get_db_connection()
    df = pd.read_sql_query(
        "SELECT company AS 'Company', description AS 'Product Description', code AS 'Product Code', color_transition AS 'Color Transition', qty_grams AS 'Quantity (grams)', remarks AS 'REMARKS' FROM indicator_inventory",
        conn
    )
    conn.close()

    st.dataframe(df)
    total_ind_g = df["Quantity (grams)"].sum() if not df.empty else 0
    c1, c2 = st.columns(2)
    c1.metric("Total Weight (Grams)", f"{total_ind_g:,.0f} g")
    c2.metric("Total Weight (KG)", f"{total_ind_g / 1000:,.2f} kg")

# --- TAB 7: TRANSACTIONS (IN/OUT UPDATES) ---
with tab7:
    st.subheader("⚡ Update Inventory Quantities (Stock IN / Stock OUT)")
    
    category = st.selectbox(
        "Select Section to Update:",
        [
            "1. Paper Roll Inventory",
            "2. Poly Inventory",
            "3. Ink Stock (Normal)",
            "4. Paper Sheet Inventory",
            "5. Corrugated Boxes",
            "6. Core Specifications",
            "7. Indicator Colour",
        ],
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    if category == "1. Paper Roll Inventory":
        items = pd.read_sql_query("SELECT id, material || ' | ' || size_gsm AS label FROM paper_roll_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Paper Roll Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Rolls Quantity", min_value=1, step=1)

            if st.button("Update Paper Roll Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE paper_roll_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Paper Roll Stock updated successfully!")
                st.rerun()

    elif category == "2. Poly Inventory":
        items = pd.read_sql_query("SELECT id, material || ' | ' || size_spec AS label FROM poly_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Poly Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Rolls Quantity", min_value=1, step=1)

            if st.button("Update Poly Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE poly_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Poly Stock updated successfully!")
                st.rerun()

    elif category == "3. Ink Stock (Normal)":
        items = pd.read_sql_query("SELECT id, colour || ' (Code: ' || code || ')' AS label FROM ink_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Ink", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Grams Quantity", min_value=1.0, step=100.0)

            if st.button("Update Ink Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE ink_inventory SET qty_grams = MAX(0, qty_grams {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Ink Stock updated successfully!")
                st.rerun()

    elif category == "4. Paper Sheet Inventory":
        items = pd.read_sql_query("SELECT id, material || ' (' || size || ')' AS label FROM paper_sheet_inventory", conn)
        if not items.empty:
            selected = st.selectbox("Select Sheet Item", items["label"])
            selected_id = int(items[items["label"] == selected]["id"].values[0])
            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Sheet Quantity", min_value=1, step=100)

            if st.button("Update Sheet Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(f"UPDATE paper_sheet_inventory SET qty_sheets = MAX(0, qty_sheets {op} ?) WHERE id = ?", (qty, selected_id))
                conn.commit()
                st.success("Paper Sheet Stock updated successfully!")
                st.rerun()

    elif category == "5. Corrugated Boxes":
        items = pd.read_sql_query("SELECT id, box_spec FROM box_inventory", conn)
        import pandas as pd
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="Rai Factory - Stock Management", layout="wide", page_icon="📦"
)

# ---------------------------------------------------------
# DATABASE SETUP & INITIALIZATION
# ---------------------------------------------------------
DB_NAME = "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS poly_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material TEXT NOT NULL,
            size_spec TEXT NOT NULL,
            qty_rolls INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS box_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_spec TEXT NOT NULL,
            unit TEXT DEFAULT 'Pcs',
            stock_qty INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indicator_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remark TEXT NOT NULL,
            qty_grams REAL DEFAULT 0.0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM poly_inventory")
    if cursor.fetchone()[0] == 0:
        poly_initial = [
            ("Blue Film (46micron)", "410×2500 mtr", 14),
            ("Blue Film (46micron)", "410×1200 mtr", 4),
            ("Blue Film (46micron)", "410×1600 mtr", 1),
            ("Blue Film (46micron)", "410×1500 mtr", 1),
            ("Blue Film (46micron)", "310×2100 mtr", 3),
            ("Blue Film (46micron)", "360×2100 mtr", 11),
            ("Blue Film (46micron)", "510×2000 mtr", 7),
            ("Blue Film (46micron)", "510×1700 mtr", 2),
            ("Blue Film (46micron)", "510×1550 mtr", 16),
            ("Blue Film (46micron)", "610×1350 mtr", 37),
            ("Blue Film (46micron)", "930×1600 mtr", 5),
            ("Blue Film (46micron)", "930×1370 mtr", 1),
            ("Blue Film (46micron)", "930×790 mtr", 1),
            ("Tyvek Film", "930×2200 mtr", 1),
            ("White Film (62micron)", "410×1285 mtr", 7),
            ("White Film (62micron)", "510×1285 mtr", 7),
            ("White Film (46micron)", "570×1950 mtr", 2),
            ("White Film (46micron)", "570×1750 mtr", 6),
            ("White Film (46micron)", "570×1600 mtr", 2),
            ("White Film (46micron)", "410×2080 mtr", 13),
            ("White Film (46micron)", "610×1480 mtr", 13),
            ("White Film (46micron)", "1000×1700 mtr", 6),
            ("Tyvek Film", "840×3000 mtr", 0),
        ]
        cursor.executemany(
            "INSERT INTO poly_inventory (material, size_spec, qty_rolls) VALUES (?, ?, ?)",
            poly_initial,
        )

    cursor.execute("SELECT COUNT(*) FROM box_inventory")
    if cursor.fetchone()[0] == 0:
        box_initial = [
            ("Ayka Small Printed Reel Box (44*23*32)", "Pcs", 654),
            ("Ayka Large Printed Reel Box (44*23*42)", "Pcs", 420),
            ("Ayka Large printed wrap Box (44*23*42)", "Pcs", 0),
            ("Bowie Dick Inner box", "Pcs", 11863),
            ("Bowie Dick Outer Box", "Pcs", 14490),
            ("Plain Bowie Dick Master Carton Box (26*24*14)", "Pcs", 540),
            ("Plain Master Carton Box for face mask (50*20*56)", "Pcs", 159),
            ("Plain small Pouch box (34*23*29)", "Pcs", 425),
            ("Plain small Autoclave box (28*26*28)", "Pcs", 380),
            ("Plain small reel box (44*23*32)", "Pcs", 524),
            ("Indicator Master Carton Box (21*18*11.5)", "Pcs", 600),
        ]
        cursor.executemany(
            "INSERT INTO box_inventory (box_spec, unit, stock_qty) VALUES (?, ?, ?)",
            box_initial,
        )

    cursor.execute("SELECT COUNT(*) FROM indicator_inventory")
    if cursor.fetchone()[0] == 0:
        indicator_initial = [
            ("LABEL (Brown)", 4734.0),
            ("REEL (Brown)", 7220.0),
            ("TYVEK REEL", 1300.0),
            ("LABEL", 700.0),
            ("LABEL", 13900.0),
            ("INDICATOR", 8700.0),
            ("REEL", 1260.0),
            ("INDICATOR / BD T...", 5700.0),
            ("INDICATOR (Red)", 990.0),
        ]
        cursor.executemany(
            "INSERT INTO indicator_inventory (remark, qty_grams) VALUES (?, ?)",
            indicator_initial,
        )

    conn.commit()
    conn.close()


init_db()

# ---------------------------------------------------------
# APP INTERFACE
# ---------------------------------------------------------
st.title("🏭 Rai Factory - Complete Stock Management")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1. Poly Inventory",
        "2. Corrugated Boxes",
        "3. Indicator Colour",
        "⚡ Stock Transactions (IN/OUT)",
    ]
)

# Poly Tab
with tab1:
    st.subheader("Poly Inventory Stock")
    search_poly = st.text_input(
        "🔍 Search Poly Material / Specification:", key="poly_search"
    )

    conn = get_db_connection()
    if search_poly:
        query = "SELECT material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory WHERE material LIKE ? OR size_spec LIKE ?"
        df_poly = pd.read_sql_query(
            query, conn, params=(f"%{search_poly}%", f"%{search_poly}%")
        )
    else:
        df_poly = pd.read_sql_query(
            "SELECT material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory",
            conn,
        )
    conn.close()

    st.dataframe(df_poly)
    st.metric("Total Poly Rolls", int(df_poly["Qty (Rolls)"].sum() if not df_poly.empty else 0))

# Box Tab
with tab2:
    st.subheader("Corrugated Boxes & Core Inventory")
    search_box = st.text_input(
        "🔍 Search Box Specification:", key="box_search"
    )

    conn = get_db_connection()
    if search_box:
        query = "SELECT box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory WHERE box_spec LIKE ?"
        df_box = pd.read_sql_query(query, conn, params=(f"%{search_box}%",))
    else:
        df_box = pd.read_sql_query(
            "SELECT box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory",
            conn,
        )
    conn.close()

    st.dataframe(df_box)
    st.metric("Total Corrugated Boxes (Pcs)", int(df_box["Stock Qty"].sum() if not df_box.empty else 0))

# Indicator Tab
with tab3:
    st.subheader("Indicator Colour (Grams)")
    conn = get_db_connection()
    df_ind = pd.read_sql_query(
        "SELECT remark AS 'Remark / Type', qty_grams AS 'Quantity (grams)' FROM indicator_inventory",
        conn,
    )
    conn.close()

    st.dataframe(df_ind)
    total_grams = df_ind["Quantity (grams)"].sum() if not df_ind.empty else 0
    col1, col2 = st.columns(2)
    col1.metric("Total Weight (Grams)", f"{total_grams:,.0f} g")
    col2.metric("Total Weight (KG)", f"{total_grams / 1000:,.2f} kg")

# Update Tab
with tab4:
    st.subheader("Update Inventory Quantities")
    category = st.radio(
        "Select Section to Update:",
        ["Poly Inventory", "Corrugated Boxes", "Indicator Colour"],
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    if category == "Poly Inventory":
        items = pd.read_sql_query(
            "SELECT id, material || ' | ' || size_spec AS label FROM poly_inventory",
            conn,
        )
        if not items.empty:
            selected = st.selectbox("Select Item", items["label"])
            selected_id = items[items["label"] == selected]["id"].values[0]

            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Rolls Quantity", min_value=1, step=1)

            if st.button("Update Poly Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(
                    f"UPDATE poly_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?",
                    (qty, selected_id),
                )
                conn.commit()
                st.success("Poly stock updated successfully!")
                st.rerun()

    elif category == "Corrugated Boxes":
        items = pd.read_sql_query(
            "SELECT id, box_spec FROM box_inventory", conn
        )
        if not items.empty:
            selected = st.selectbox("Select Box Item", items["box_spec"])
            selected_id = items[items["box_spec"] == selected]["id"].values[0]

            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Pcs Quantity", min_value=1, step=1)

            if st.button("Update Box Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(
                    f"UPDATE box_inventory SET stock_qty = MAX(0, stock_qty {op} ?) WHERE id = ?",
                    (qty, selected_id),
                )
                conn.commit()
                st.success("Box stock updated successfully!")
                st.rerun()

    elif category == "Indicator Colour":
        items = pd.read_sql_query(
            "SELECT id, remark FROM indicator_inventory", conn
        )
        if not items.empty:
            selected = st.selectbox("Select Indicator Type", items["remark"])
            selected_id = items[items["remark"] == selected]["id"].values[0]

            action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
            qty = st.number_input("Grams Quantity", min_value=1.0, step=10.0)

            if st.button("Update Indicator Stock"):
                op = "+" if action == "Stock IN (+)" else "-"
                cursor.execute(
                    f"UPDATE indicator_inventory SET qty_grams = MAX(0, qty_grams {op} ?) WHERE id = ?",
                    (qty, selected_id),
                )
                conn.commit()
                st.success("Indicator colour stock updated successfully!")
                st.rerun()

    conn.close()import pandas as pd
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="Rai Factory - Stock Management", layout="wide", page_icon="📦"
)

# ---------------------------------------------------------
# DATABASE SETUP & INITIALIZATION
# ---------------------------------------------------------
DB_NAME = "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Poly Inventory
    cursor.execute(""" CREATE TABLE IF NOT EXISTS poly_inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT, material TEXT NOT NULL, size_spec TEXT NOT NULL, qty_rolls INTEGER DEFAULT 0 ) """)

    # Corrugated Boxes
    cursor.execute(""" CREATE TABLE IF NOT EXISTS box_inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT, box_spec TEXT NOT NULL, unit TEXT DEFAULT 'Pcs', stock_qty INTEGER DEFAULT 0 ) """)

    # Indicator Colour
    cursor.execute(""" CREATE TABLE IF NOT EXISTS indicator_inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT, remark TEXT NOT NULL, qty_grams REAL DEFAULT 0.0 ) """)

    # Seed Data
    cursor.execute("SELECT COUNT(*) FROM poly_inventory")
    if cursor.fetchone()[0] == 0:
        poly_initial = [
            ("Blue Film (46micron)", "410×2500 mtr", 14),
            ("Blue Film (46micron)", "410×1200 mtr", 4),
            ("Blue Film (46micron)", "410×1600 mtr", 1),
            ("Blue Film (46micron)", "410×1500 mtr", 1),
            ("Blue Film (46micron)", "310×2100 mtr", 3),
            ("Blue Film (46micron)", "360×2100 mtr", 11),
            ("Blue Film (46micron)", "510×2000 mtr", 7),
            ("Blue Film (46micron)", "510×1700 mtr", 2),
            ("Blue Film (46micron)", "510×1550 mtr", 16),
            ("Blue Film (46micron)", "610×1350 mtr", 37),
            ("Blue Film (46micron)", "930×1600 mtr", 5),
            ("Blue Film (46micron)", "930×1370 mtr", 1),
            ("Blue Film (46micron)", "930×790 mtr", 1),
            ("Tyvek Film", "930×2200 mtr", 1),
            ("White Film (62micron)", "410×1285 mtr", 7),
            ("White Film (62micron)", "510×1285 mtr", 7),
            ("White Film (46micron)", "570×1950 mtr", 2),
            ("White Film (46micron)", "570×1750 mtr", 6),
            ("White Film (46micron)", "570×1600 mtr", 2),
            ("White Film (46micron)", "410×2080 mtr", 13),
            ("White Film (46micron)", "610×1480 mtr", 13),
            ("White Film (46micron)", "1000×1700 mtr", 6),
            ("Tyvek Film", "840×3000 mtr", 0),
        ]
        cursor.executemany(
            "INSERT INTO poly_inventory (material, size_spec, qty_rolls) VALUES (?, ?, ?)",
            poly_initial,
        )

    cursor.execute("SELECT COUNT(*) FROM box_inventory")
    if cursor.fetchone()[0] == 0:
        box_initial = [
            ("Ayka Small Printed Reel Box (44*23*32)", "Pcs", 654),
            ("Ayka Large Printed Reel Box (44*23*42)", "Pcs", 420),
            ("Ayka Large printed wrap Box (44*23*42)", "Pcs", 0),
            ("Bowie Dick Inner box", "Pcs", 11863),
            ("Bowie Dick Outer Box", "Pcs", 14490),
            ("Plain Bowie Dick Master Carton Box (26*24*14)", "Pcs", 540),
            ("Plain Master Carton Box for face mask (50*20*56)", "Pcs", 159),
            ("Plain small Pouch box (34*23*29)", "Pcs", 425),
            ("Plain small Autoclave box (28*26*28)", "Pcs", 380),
            ("Plain small reel box (44*23*32)", "Pcs", 524),
            ("Indicator Master Carton Box (21*18*11.5)", "Pcs", 600),
        ]
        cursor.executemany(
            "INSERT INTO box_inventory (box_spec, unit, stock_qty) VALUES (?, ?, ?)",
            box_initial,
        )

    cursor.execute("SELECT COUNT(*) FROM indicator_inventory")
    if cursor.fetchone()[0] == 0:
        indicator_initial = [
            ("LABEL (Brown)", 4734.0),
            ("REEL (Brown)", 7220.0),
            ("TYVEK REEL", 1300.0),
            ("LABEL", 700.0),
            ("LABEL", 13900.0),
            ("INDICATOR", 8700.0),
            ("REEL", 1260.0),
            ("INDICATOR / BD T...", 5700.0),
            ("INDICATOR (Red)", 990.0),
        ]
        cursor.executemany(
            "INSERT INTO indicator_inventory (remark, qty_grams) VALUES (?, ?)",
            indicator_initial,
        )

    conn.commit()
    conn.close()


init_db()

# ---------------------------------------------------------
# APP INTERFACE
# ---------------------------------------------------------
st.title("🏭 Rai Factory - Complete Stock Management")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1. Poly Inventory",
        "2. Corrugated Boxes",
        "3. Indicator Colour",
        "⚡ Stock Transactions (IN/OUT)",
    ]
)

# Poly Tab
with tab1:
    st.subheader("Poly Inventory Stock")
    search_poly = st.text_input(
        "🔍 Search Poly Material / Specification:", key="poly_search"
    )

    conn = get_db_connection()
    if search_poly:
        query = "SELECT id, material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory WHERE material LIKE ? OR size_spec LIKE ?"
        df_poly = pd.read_sql_query(
            query, conn, params=(f"%{search_poly}%", f"%{search_poly}%")
        )
    else:
        df_poly = pd.read_sql_query(
            "SELECT id, material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory",
            conn,
        )
    conn.close()

    st.dataframe(df_poly.drop(columns=["id"]), use_container_width=True)
    st.metric("Total Poly Rolls", int(df_poly["Qty (Rolls)"].sum()))

# Box Tab
with tab2:
    st.subheader("Corrugated Boxes & Core Inventory")
    search_box = st.text_input(
        "🔍 Search Box Specification:", key="box_search"
    )

    conn = get_db_connection()
    if search_box:
        query = "SELECT id, box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory WHERE box_spec LIKE ?"
        df_box = pd.read_sql_query(query, conn, params=(f"%{search_box}%",))
    else:
        df_box = pd.read_sql_query(
            "SELECT id, box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory",
            conn,
        )
    conn.close()

    st.dataframe(df_box.drop(columns=["id"]), use_container_width=True)
    st.metric("Total Corrugated Boxes (Pcs)", int(df_box["Stock Qty"].sum()))

# Indicator Tab
with tab3:
    st.subheader("Indicator Colour (Grams)")
    conn = get_db_connection()
    df_ind = pd.read_sql_query(
        "SELECT id, remark AS 'Remark / Type', qty_grams AS 'Quantity (grams)' FROM indicator_inventory",
        conn,
    )
    conn.close()

    st.dataframe(df_ind.drop(columns=["id"]), use_container_width=True)
    total_grams = df_ind["Quantity (grams)"].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Weight (Grams)", f"{total_grams:,.0f} g")
    col2.metric("Total Weight (KG)", f"{total_grams / 1000:,.2f} kg")

# Update Tab
with tab4:
    st.subheader("Update Inventory Quantities")
    category = st.radio(
        "Select Section to Update:",
        ["Poly Inventory", "Corrugated Boxes", "Indicator Colour"],
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    if category == "Poly Inventory":
        items = pd.read_sql_query(
            "SELECT id, material || ' | ' || size_spec AS label FROM poly_inventory",
            conn,
        )
        selected = st.selectbox("Select Item", items["label"])
        selected_id = items[items["label"] == selected]["id"].values[0]

        action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
        qty = st.number_input("Rolls Quantity", min_value=1, step=1)

        if st.button("Update Poly Stock"):
            op = "+" if action == "Stock IN (+)" else "-"
            cursor.execute(
                f"UPDATE poly_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?",
                (qty, selected_id),
            )
            conn.commit()
            st.success("Poly stock updated successfully!")
            st.rerun()

    elif category == "Corrugated Boxes":
        items = pd.read_sql_query(
            "SELECT id, box_spec FROM box_inventory", conn
        )
        selected = st.selectbox("Select Box Item", items["box_spec"])
        selected_id = items[items["box_spec"] == selected]["id"].values[0]

        action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
        qty = st.number_input("Pcs Quantity", min_value=1, step=1)

        if st.button("Update Box Stock"):
            op = "+" if action == "Stock IN (+)" else "-"
            cursor.execute(
                f"UPDATE box_inventory SET stock_qty = MAX(0, stock_qty {op} ?) WHERE id = ?",
                (qty, selected_id),
            )
            conn.commit()
            st.success("Box stock updated successfully!")
            st.rerun()

    elif category == "Indicator Colour":
        items = pd.read_sql_query(
            "SELECT id, remark FROM indicator_inventory", conn
        )
        selected = st.selectbox("Select Indicator Type", items["remark"])
        selected_id = items[items["remark"] == selected]["id"].values[0]

        action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
        qty = st.number_input("Grams Quantity", min_value=1.0, step=10.0)

        if st.button("Update Indicator Stock"):
            op = "+" if action == "Stock IN (+)" else "-"
            cursor.execute(
                f"UPDATE indicator_inventory SET qty_grams = MAX(0, qty_grams {op} ?) WHERE id = ?",
                (qty, selected_id),
            )
            conn.commit()
            st.success("Indicator colour stock updated successfully!")
            st.rerun()

    conn.close()import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Rai Factory - Stock Management", layout="wide", page_icon="📦")

# ---------------------------------------------------------
# DATABASE SETUP & INITIALIZATION
# ---------------------------------------------------------
DB_NAME = "inventory.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Poly Inventory
    cursor.execute(''' CREATE TABLE IF NOT EXISTS poly_inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT, material TEXT NOT NULL, size_spec TEXT NOT NULL, qty_rolls INTEGER DEFAULT 0 ) ''')
    
    # Corrugated Boxes
    cursor.execute(''' CREATE TABLE IF NOT EXISTS box_inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT, box_spec TEXT NOT NULL, unit TEXT DEFAULT 'Pcs', stock_qty INTEGER DEFAULT 0 ) ''')
    
    # Indicator Colour
    cursor.execute(''' CREATE TABLE IF NOT EXISTS indicator_inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT, remark TEXT NOT NULL, qty_grams REAL DEFAULT 0.0 ) ''')
    
    # Seed Data
    cursor.execute('SELECT COUNT(*) FROM poly_inventory')
    if cursor.fetchone()[0] == 0:
        poly_initial = [
            ("Blue Film (46micron)", "410×2500 mtr", 14),
            ("Blue Film (46micron)", "410×1200 mtr", 4),
            ("Blue Film (46micron)", "410×1600 mtr", 1),
            ("Blue Film (46micron)", "410×1500 mtr", 1),
            ("Blue Film (46micron)", "310×2100 mtr", 3),
            ("Blue Film (46micron)", "360×2100 mtr", 11),
            ("Blue Film (46micron)", "510×2000 mtr", 7),
            ("Blue Film (46micron)", "510×1700 mtr", 2),
            ("Blue Film (46micron)", "510×1550 mtr", 16),
            ("Blue Film (46micron)", "610×1350 mtr", 37),
            ("Blue Film (46micron)", "930×1600 mtr", 5),
            ("Blue Film (46micron)", "930×1370 mtr", 1),
            ("Blue Film (46micron)", "930×790 mtr", 1),
            ("Tyvek Film", "930×2200 mtr", 1),
            ("White Film (62micron)", "410×1285 mtr", 7),
            ("White Film (62micron)", "510×1285 mtr", 7),
            ("White Film (46micron)", "570×1950 mtr", 2),
            ("White Film (46micron)", "570×1750 mtr", 6),
            ("White Film (46micron)", "570×1600 mtr", 2),
            ("White Film (46micron)", "410×2080 mtr", 13),
            ("White Film (46micron)", "610×1480 mtr", 13),
            ("White Film (46micron)", "1000×1700 mtr", 6),
            ("Tyvek Film", "840×3000 mtr", 0)
        ]
        cursor.executemany('INSERT INTO poly_inventory (material, size_spec, qty_rolls) VALUES (?, ?, ?)', poly_initial)

    cursor.execute('SELECT COUNT(*) FROM box_inventory')
    if cursor.fetchone()[0] == 0:
        box_initial = [
            ("Ayka Small Printed Reel Box (44*23*32)", "Pcs", 654),
            ("Ayka Large Printed Reel Box (44*23*42)", "Pcs", 420),
            ("Ayka Large printed wrap Box (44*23*42)", "Pcs", 0),
            ("Bowie Dick Inner box", "Pcs", 11863),
            ("Bowie Dick Outer Box", "Pcs", 14490),
            ("Plain Bowie Dick Master Carton Box (26*24*14)", "Pcs", 540),
            ("Plain Master Carton Box for face mask (50*20*56)", "Pcs", 159),
            ("Plain small Pouch box (34*23*29)", "Pcs", 425),
            ("Plain small Autoclave box (28*26*28)", "Pcs", 380),
            ("Plain small reel box (44*23*32)", "Pcs", 524),
            ("Indicator Master Carton Box (21*18*11.5)", "Pcs", 600)
        ]
        cursor.executemany('INSERT INTO box_inventory (box_spec, unit, stock_qty) VALUES (?, ?, ?)', box_initial)

    cursor.execute('SELECT COUNT(*) FROM indicator_inventory')
    if cursor.fetchone()[0] == 0:
        indicator_initial = [
            ("LABEL (Brown)", 4734.0),
            ("REEL (Brown)", 7220.0),
            ("TYVEK REEL", 1300.0),
            ("LABEL", 700.0),
            ("LABEL", 13900.0),
            ("INDICATOR", 8700.0),
            ("REEL", 1260.0),
            ("INDICATOR / BD T...", 5700.0),
            ("INDICATOR (Red)", 990.0)
        ]
        cursor.executemany('INSERT INTO indicator_inventory (remark, qty_grams) VALUES (?, ?)', indicator_initial)

    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# APP INTERFACE
# ---------------------------------------------------------
st.title("🏭 Rai Factory - Complete Stock Management")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Poly Inventory", 
    "2. Corrugated Boxes", 
    "3. Indicator Colour", 
    "⚡ Stock Transactions (IN/OUT)"
])

# Poly Tab
with tab1:
    st.subheader("Poly Inventory Stock")
    search_poly = st.text_input("🔍 Search Poly Material / Specification:", key="poly_search")
    
    conn = get_db_connection()
    if search_poly:
        query = "SELECT id, material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory WHERE material LIKE ? OR size_spec LIKE ?"
        df_poly = pd.read_sql_query(query, conn, params=(f"%{search_poly}%", f"%{search_poly}%"))
    else:
        df_poly = pd.read_sql_query("SELECT id, material AS 'Material', size_spec AS 'Size / Specification', qty_rolls AS 'Qty (Rolls)' FROM poly_inventory", conn)
    conn.close()

    st.dataframe(df_poly.drop(columns=['id']), use_container_width=True)
    st.metric("Total Poly Rolls", int(df_poly['Qty (Rolls)'].sum()))

# Box Tab
with tab2:
    st.subheader("Corrugated Boxes & Core Inventory")
    search_box = st.text_input("🔍 Search Box Specification:", key="box_search")
    
    conn = get_db_connection()
    if search_box:
        query = "SELECT id, box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory WHERE box_spec LIKE ?"
        df_box = pd.read_sql_query(query, conn, params=(f"%{search_box}%",))
    else:
        df_box = pd.read_sql_query("SELECT id, box_spec AS 'Box Type & Specifications', unit AS 'Unit', stock_qty AS 'Stock Qty' FROM box_inventory", conn)
    conn.close()

    st.dataframe(df_box.drop(columns=['id']), use_container_width=True)
    st.metric("Total Corrugated Boxes (Pcs)", int(df_box['Stock Qty'].sum()))

# Indicator Tab
with tab3:
    st.subheader("Indicator Colour (Grams)")
    conn = get_db_connection()
    df_ind = pd.read_sql_query("SELECT id, remark AS 'Remark / Type', qty_grams AS 'Quantity (grams)' FROM indicator_inventory", conn)
    conn.close()

    st.dataframe(df_ind.drop(columns=['id']), use_container_width=True)
    total_grams = df_ind['Quantity (grams)'].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Weight (Grams)", f"{total_grams:,.0f} g")
    col2.metric("Total Weight (KG)", f"{total_grams / 1000:,.2f} kg")

# Update Tab
with tab4:
    st.subheader("Update Inventory Quantities")
    category = st.radio("Select Section to Update:", ["Poly Inventory", "Corrugated Boxes", "Indicator Colour"])
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if category == "Poly Inventory":
        items = pd.read_sql_query("SELECT id, material || ' | ' || size_spec AS label FROM poly_inventory", conn)
        selected = st.selectbox("Select Item", items['label'])
        selected_id = items[items['label'] == selected]['id'].values[0]
        
        action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
        qty = st.number_input("Rolls Quantity", min_value=1, step=1)
        
        if st.button("Update Poly Stock"):
            op = "+" if action == "Stock IN (+)" else "-"
            cursor.execute(f"UPDATE poly_inventory SET qty_rolls = MAX(0, qty_rolls {op} ?) WHERE id = ?", (qty, selected_id))
            conn.commit()
            st.success("Poly stock updated successfully!")
            st.rerun()

    elif category == "Corrugated Boxes":
        items = pd.read_sql_query("SELECT id, box_spec FROM box_inventory", conn)
        selected = st.selectbox("Select Box Item", items['box_spec'])
        selected_id = items[items['box_spec'] == selected]['id'].values[0]
        
        action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
        qty = st.number_input("Pcs Quantity", min_value=1, step=1)
        
        if st.button("Update Box Stock"):
            op = "+" if action == "Stock IN (+)" else "-"
            cursor.execute(f"UPDATE box_inventory SET stock_qty = MAX(0, stock_qty {op} ?) WHERE id = ?", (qty, selected_id))
            conn.commit()
            st.success("Box stock updated successfully!")
            st.rerun()

    elif category == "Indicator Colour":
        items = pd.read_sql_query("SELECT id, remark FROM indicator_inventory", conn)
        selected = st.selectbox("Select Indicator Type", items['remark'])
        selected_id = items[items['remark'] == selected]['id'].values[0]
        
        action = st.radio("Action", ["Stock IN (+)", "Stock OUT (-)"])
        qty = st.number_input("Grams Quantity", min_value=1.0, step=10.0)
        
        if st.button("Update Indicator Stock"):
            op = "+" if action == "Stock IN (+)" else "-"
            cursor.execute(f"UPDATE indicator_inventory SET qty_grams = MAX(0, qty_grams {op} ?) WHERE id = ?", (qty, selected_id))
            conn.commit()
            st.success("Indicator colour stock updated successfully!")
            st.rerun()

    conn.close()Dim fso, shell, desktopPath, dbPath, accessApp
Set shell = CreateObject("WScript.Shell")
desktopPath = shell.SpecialFolders("Desktop")
dbPath = desktopPath & "\Ayka_Stock_Inventory.accdb"

Set fso = CreateObject("Scripting.FileSystemObject")
If fso.FileExists(dbPath) Then fso.DeleteFile(dbPath)

On Error Resume Next
Set accessApp = CreateObject("Access.Application")
If accessApp Is Nothing Then
    MsgBox "Microsoft Access is not installed on this system.", 16, "Error"
    WScript.Quit
End If

accessApp.NewCurrentDatabase dbPath
Dim db
Set db = accessApp.CurrentDb

' 1. Paper_Roll_Inventory
db.Execute "CREATE TABLE Paper_Roll_Inventory (ID COUNTER PRIMARY KEY, Material_Name VARCHAR(100), Size_GSM VARCHAR(100), Qty_Rolls INT);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Medi-Craft', '410x3000 mtr (60 GSM)', 4);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Medi-Craft', '610x3000 mtr (60 GSM)', 21);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Medi-Craft', '610x2000 mtr (60 GSM)', 2);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Medi-Craft', '930x2000 mtr (60 GSM)', 1);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Medi-Craft', '420x2000 mtr (60 GSM)', 0);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Pelta Med', '610x3500 mtr (62 GSM)', 49);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Pelta Med', '410x3500 mtr (62 GSM)', 32);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Pelta Med', '930x3500 mtr (62 GSM)', 5);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Pelta Med', '570x3500 mtr (62 GSM)', 8);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Pelta Med', '930x3500 mtr (68 GSM)', 11);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Pelta Med', '610x2400 mtr (68 GSM)', 11);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Shivshakti Piggybag', '200x700 mtr (300gsm)', 4);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Shivshakti Piggybag', '200x1000 mtr (300gsm)', 23);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Filter Face Mask', '175x2000 mtr', 45);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('White Mask Roll', '175x2000 mtr', 30);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Blue Mask Roll', '190x2000 mtr', 25);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Elastic Roll', '190 (90gsm)', 9);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Avory Roll', '100x680 mtr (300gsm)', 11);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Avory Roll', '200x680 mtr (300gsm)', 0);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Avary Roll', '300x1000 mtr (300gsm)', 2);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Tyvek Roll', '1100x1000 mtr', 0);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('Autoclave ROLL', '912x1000 mtr.', 0);"
db.Execute "INSERT INTO Paper_Roll_Inventory (Material_Name, Size_GSM, Qty_Rolls) VALUES ('ETO ROLL', '912x1000 mtr', 0);"

' 2. Poly_Inventory
db.Execute "CREATE TABLE Poly_Inventory (ID COUNTER PRIMARY KEY, Material_Name VARCHAR(100), Size_Specification VARCHAR(100), Qty_Rolls INT);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '410x2500 mtr', 14);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '410x1200 mtr', 4);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '410x1600 mtr', 1);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '410x1500 mtr', 1);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '310x2100 mtr', 3);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '360x2100 mtr', 11);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '510x2000 mtr', 7);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '510x1700 mtr', 2);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '510x1550 mtr', 16);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '610x1350 mtr', 37);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '930x1600 mtr', 5);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '930x1370 mtr', 1);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Blue Film (46micron)', '930x790 mtr', 1);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Tyvek Film', '930x2200 mtr', 1);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (62micron)', '410x1285 mtr', 7);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (62micron)', '510x1285 mtr', 7);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (46micron)', '570x1950 mtr', 2);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (46micron)', '570x1750 mtr', 6);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (46micron)', '570x1600 mtr', 2);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (46micron)', '410x2080 mtr', 13);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (46micron)', '610x1480 mtr', 13);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('White Film (46micron)', '1000x1700 mtr', 6);"
db.Execute "INSERT INTO Poly_Inventory (Material_Name, Size_Specification, Qty_Rolls) VALUES ('Tyvek Film', '840x3000 mtr', 0);"

' 3. Ink_Stock_Normal
db.Execute "CREATE TABLE Ink_Stock_Normal (ID COUNTER PRIMARY KEY, Colour VARCHAR(50), Code VARCHAR(50), Qty_Grams DOUBLE);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Purple', '5133', 7300);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Dark Blue', '10610', 3800);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Blue', '2640', 5200);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Blue', '0', 5000);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Metallic Blue', '2325', 4580);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Sky Blue', '10611', 3780);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Black', '0', 2000);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('TEST Medium', '0', 5100);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Violet blue', '8667', 5720);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Green', '2819', 4970);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Magenta', '10522', 4850);"
db.Execute "INSERT INTO Ink_Stock_Normal (Colour, Code, Qty_Grams) VALUES ('Lemon Yellow', '10521', 16520);"

' 4. Paper_Sheet_Inventory
db.Execute "CREATE TABLE Paper_Sheet_Inventory (ID COUNTER PRIMARY KEY, Material_Name VARCHAR(100), Unit_Type VARCHAR(20), Qty_Sheets INT);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('SHIV SHAKTI Gumming Paper', 'Sheets', 10612);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('SHIV SHAKTI Paper(Bowie Dick)', 'Sheets', 1263);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('A4 Paper', 'Sheets', 4687);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('Lot Sheet', 'Sheets', 107000);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('Card Sheet', 'Sheets', 0);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('Green Paper', 'Sheets', 1309);"
db.Execute "INSERT INTO Paper_Sheet_Inventory (Material_Name, Unit_Type, Qty_Sheets) VALUES ('Acrylic Paper', 'Sheets', 160);"

' 5. Packaging_Core_Inventory
db.Execute "CREATE TABLE Packaging_Core_Inventory (ID COUNTER PRIMARY KEY, Item_Category VARCHAR(50), Specification VARCHAR(150), Unit VARCHAR(20), Stock_Qty INT);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Ayka Small Printed Reel Box (44*23*32)', 'Pcs', 654);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Ayka Large Printed Reel box (44*23*42)', 'Pcs', 420);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Ayka Large printed wrap box (44*23*42)', 'Pcs', 0);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Bowie Dick Inner box', 'Pcs', 11863);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Bowie Dick Outer Box', 'Pcs', 14490);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Plain Bowie Dick Master Carton Box (26*24*14)', 'Pcs', 540);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Plain Master Carton Box for face mask (50*20*50)', 'pcs', 159);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Plain small Pouch box (34*23*29)', 'Pcs', 425);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Plain small Autoclave box (28*26*28)', 'pcs', 380);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Plain small reel box (44*23*32)', 'pcs', 524);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Corrugated Box', 'Indicator Master Carton Box (21*18*11.5)', 'pcs', 600);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (55mm)', 'Pcs', 450);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (75mm)', 'Pcs', 165);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (100mm)', 'Pcs', 906);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (125mm)', 'Pcs', 154);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (150mm)', 'Pcs', 1270);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (200mm)', 'Pcs', 826);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (250mm)', 'Pcs', 670);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (300mm)', 'Pcs', 36);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (350mm)', 'Pcs', 277);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (400mm)', 'Pcs', 461);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Cardboard Core', 'Cardboard Core (500mm)', 'Pcs', 190);"
db.Execute "INSERT INTO Packaging_Core_Inventory (Item_Category, Specification, Unit, Stock_Qty) VALUES ('Plastic Core', 'Core Plastic (32mm)', 'Pcs', 82280);"

' 6. Change_Indicator_Inks
db.Execute "CREATE TABLE Change_Indicator_Inks (ID COUNTER PRIMARY KEY, Company VARCHAR(50), Product_Description VARCHAR(100), Product_Code VARCHAR(100), Color_Transition VARCHAR(100), Qty_Grams DOUBLE, Remarks VARCHAR(100));"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Chroma inks', 'ETO - Yellow', 'CL/FYC/EO/4', 'Yellow to brown', 4734, 'LABEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Chroma Inks', 'ETO - Pink', 'CL/FRC/EO/2', 'Pink To Brown', 7220, 'REEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Chroma Inks', 'Plasma - Red', 'CL/FRY/PLA/2', 'Red', 1300, 'TYVEK REEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Tempil Ink', 'Steam Green', 'TISFRG1010GL-27566', 'Green', 700, 'LABEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Tempil Ink', 'Steam Green', 'TIS784-B/858.ACT/GL-27505', 'Green', 13900, 'LABEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Tempil Ink', 'Steam-Blue', 'TISFAC858.1GL-27518', 'Blue', 8700, 'INDICATOR');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Tempil ink', 'Steam - Blue', 'TISFAC663GL--27510', 'Blue', 1260, 'REEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('Tempil Ink', 'Steam-Pink', 'TISFRC7848.2GL-27539', 'Pink', 5700, 'INDICATOR/BD TEST Sheet');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('OTS', 'Plasma - Blue', 'VH202-BR', 'Blue to red', 990, 'INDICATOR (TRIAL)');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('OTS', 'Steam-PB', 'STEAMPB-', 'Purple to Green', 8500, 'LABEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('OTS', 'Plasma - Red', 'VH202-RY', 'Red To Yellow', 7700, 'INDICATOR');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('OTS', 'ETO - Yellow', 'EO-YB', 'Yellow to brown', 5500, 'LABEL');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('OTS', 'Formaldehyde - Red', 'HCHO-RG', 'Red to Green', 5200, '');"
db.Execute "INSERT INTO Change_Indicator_Inks (Company, Product_Description, Product_Code, Color_Transition, Qty_Grams, Remarks) VALUES ('OTS', 'China Pink', 'STEAM-RB', '', 3370, '');"

accessApp.CloseCurrentDatabase
accessApp.Quit
MsgBox "Database 'Ayka_Stock_Inventory.accdb' successfully created on Desktop!", 64, "Success"import sqlite3
import pandas as pd
from github import Github

# Initialize Database
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER DEFAULT 0,
            unit TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Export DB to Excel & Sync with GitHub
def sync_to_github(token, repo_name, file_path="stock_report.xlsx"):
    # Read from SQLite to Pandas DataFrame
    conn = sqlite3.connect('inventory.db')
    df = pd.read_sql_query("SELECT * FROM stock", conn)
    conn.close()
    
    # Save as Excel
    df.to_excel(file_path, index=False)
    
    # Push to GitHub
    g = Github(token)
    repo = g.get_user().get_repo(repo_name)
    
    with open(file_path, 'rb') as f:
        content = f.read()
        
    try:
        existing_file = repo.get_contents(file_path)
        repo.update_file(existing_file.path, "Auto-update stock report", content, existing_file.sha)
        print("Stock report successfully updated on GitHub!")
    except Exception:
        repo.create_file(file_path, "Initial stock report upload", content)
        print("Stock report created on GitHub!")

if __name__ == "__main__":
    init_db()
