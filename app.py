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
            qty = st.number_input("Box Quantity (Pcs)", min_value=1, step=1)

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

    conn.close()        (r.category,r.item_name,r.specification,r.unit,float(r.opening_qty),
         float(r.reorder_level),"",datetime.now().isoformat()))
    con.commit()

def inventory():
    return pd.read_sql_query("SELECT * FROM inventory ORDER BY category,item_name", con)

def header(title, subtitle):
    st.markdown(f"""<div class="topbar"> <div class="title">{title}</div><div class="sub">{subtitle}</div></div>""", unsafe_allow_html=True)

# ---------- Login ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = ""

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,1.2,1])
    with c2:
        st.markdown(""" <div class="topbar" style="text-align:center;padding:35px 25px;"> <div style="font-size:36px;">ðŸ“¦</div> <div class="title">RAI FACTORY</div> <div class="sub">ENTERPRISE RESOURCE PLANNING</div> </div>""", unsafe_allow_html=True)
        user = st.text_input("User ID", placeholder="Enter user ID")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("Sign In", type="primary", use_container_width=True):
            # Demo credentials; change these before production deployment.
            users = {"admin":"admin123", "store":"store123", "production":"prod123"}
            if users.get(user) == password:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid User ID or Password")
        st.caption("Demo: admin / admin123")
    st.stop()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand">RAI FACTORY</div><div class="brand2">ERP â€¢ INVENTORY â€¢ PRODUCTION</div>', unsafe_allow_html=True)
    st.divider()
    st.caption("MAIN MENU")
    menu = st.radio("", [
        "Dashboard","Inventory","Stock Issue / Receipt",
        "Production & Job Cards","Procurement","MIS Reports"
    ])
    st.divider()
    st.caption(f"Signed in as: {st.session_state.user}")
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    st.caption(datetime.now().strftime("%d %b %Y â€¢ %I:%M %p"))
    st.caption("RAI ERP Professional v2.0")

d = inventory()
low = d[(d.reorder_level > 0) & (d.qty <= d.reorder_level)]
zero = d[d.qty <= 0]

# ---------- Dashboard ----------
if menu == "Dashboard":
    header("Executive Dashboard", "Inventory, production and procurement overview")
    a,b,c,d1 = st.columns(4)
    a.markdown(f'<div class="kpi"><div class="kpi-label">Inventory Items</div><div class="kpi-value">{len(d):,}</div><div class="kpi-note">Master records</div></div>', unsafe_allow_html=True)
    b.markdown(f'<div class="kpi"><div class="kpi-label">Categories</div><div class="kpi-value">{d.category.nunique():,}</div><div class="kpi-note">Material groups</div></div>', unsafe_allow_html=True)
    c.markdown(f'<div class="kpi"><div class="kpi-label">Reorder Alerts</div><div class="kpi-value">{len(low):,}</div><div class="kpi-note">Purchase attention</div></div>', unsafe_allow_html=True)
    d1.markdown(f'<div class="kpi"><div class="kpi-label">Zero Stock</div><div class="kpi-value">{len(zero):,}</div><div class="kpi-note">Immediate action</div></div>', unsafe_allow_html=True)

    left,right = st.columns([1.45,1])
    with left:
        st.markdown('<div class="section">Stock by Category</div>', unsafe_allow_html=True)
        if len(d):
            st.bar_chart(d.groupby("category")["qty"].sum().sort_values(ascending=False))
    with right:
        st.markdown('<div class="section">Critical Alerts</div>', unsafe_allow_html=True)
        if len(zero):
            st.markdown(f'<div class="alert">âš  {len(zero)} item(s) have zero stock.</div>', unsafe_allow_html=True)
            st.dataframe(zero[["item_name","qty","unit","lot_no"]].head(12), use_container_width=True, hide_index=True)
        elif len(low):
            st.markdown(f'<div class="alert">âš  {len(low)} item(s) are below reorder level.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="good">âœ“ No configured stock alerts.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">Current Stock Position</div>', unsafe_allow_html=True)
    st.dataframe(d[["category","item_name","specification","qty","unit","reorder_level","lot_no"]].head(30),
                 use_container_width=True, hide_index=True)

# ---------- Inventory ----------
elif menu == "Inventory":
    header("Inventory Master", "Raw materials, packing materials, consumables and finished stock")
    a,b,c = st.columns([1.4,1,1])
    search = a.text_input("Search", placeholder="Item / specification / lot")
    cat = b.selectbox("Category", ["All"] + sorted(d.category.dropna().unique()))
    status = c.selectbox("Status", ["All","Available","Low Stock","Zero Stock"])
    v = d.copy()
    if search:
        m = v.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False))
        v = v[m.any(axis=1)]
    if cat != "All": v = v[v.category == cat]
    if status == "Available": v = v[v.qty > 0]
    if status == "Zero Stock": v = v[v.qty <= 0]
    if status == "Low Stock": v = v[(v.reorder_level > 0) & (v.qty <= v.reorder_level)]
    st.caption(f"{len(v):,} records")
    st.dataframe(v[["id","category","item_name","specification","unit","qty","reorder_level","lot_no","updated_at"]],
                 use_container_width=True, hide_index=True)
    st.download_button("Export Inventory", v.to_csv(index=False).encode(), "inventory.csv", "text/csv")

    with st.expander("ï¼‹ Add New Inventory Item"):
        with st.form("add"):
            a,b,c = st.columns(3)
            cat2 = a.text_input("Category")
            item = b.text_input("Item Name")
            spec = c.text_input("Specification")
            a,b,c,d1 = st.columns(4)
            unit = a.text_input("Unit","Pcs")
            qty = b.number_input("Opening Qty", min_value=0.0)
            reorder = c.number_input("Reorder Level", min_value=0.0)
            lot = d1.text_input("Lot No.")
            if st.form_submit_button("Save Item", type="primary") and item:
                con.execute("""INSERT INTO inventory (category,item_name,specification,unit,qty,reorder_level,lot_no,updated_at) VALUES(?,?,?,?,?,?,?,?)""",
                (cat2,item,spec,unit,qty,reorder,lot,datetime.now().isoformat()))
                con.commit()
                st.success("Item added successfully.")

# ---------- Stock Transactions ----------
elif menu == "Stock Issue / Receipt":
    header("Stock Issue / Receipt", "Controlled stock movement with job card and responsibility tracking")
    if len(d) == 0:
        st.warning("No inventory records found.")
    else:
        labels = {f"{r.id} â€¢ {r.item_name} â€¢ {r.specification}":r.id for r in d.itertuples()}
        choice = st.selectbox("Select Material", list(labels))
        item_id = labels[choice]
        row = d[d.id == item_id].iloc[0]
        st.info(f"Current Balance: **{row.qty:g} {row.unit}**")
        with st.form("txn"):
            a,b,c = st.columns(3)
            typ = a.selectbox("Transaction",["RECEIPT","ISSUE","ADJUSTMENT"])
            qty = b.number_input("Quantity",min_value=0.0,value=1.0)
            ref = c.text_input("Job Card / Reference")
            a,b,c = st.columns(3)
            person = a.text_input("Issued / Received By")
            remarks = b.text_input("Remarks")
            tdate = c.date_input("Date",date.today())
            if st.form_submit_button("Post Transaction",type="primary"):
                new = row.qty + qty if typ=="RECEIPT" else row.qty-qty if typ=="ISSUE" else qty
                if new < 0:
                    st.error("Insufficient stock.")
                else:
                    con.execute("UPDATE inventory SET qty=?,updated_at=? WHERE id=?",(new,datetime.now().isoformat(),item_id))
                    con.execute("""INSERT INTO transactions (trans_date,trans_type,item_id,qty,reference,person,remarks) VALUES(?,?,?,?,?,?,?)""",(str(tdate),typ,item_id,qty,ref,person,remarks))
                    con.commit()
                    st.success(f"Posted successfully. New balance: {new:g} {row.unit}")

    st.markdown('<div class="section">Recent Transactions</div>', unsafe_allow_html=True)
    tx = pd.read_sql_query("""SELECT t.trans_date,t.trans_type,i.item_name, i.specification,t.qty,i.unit,t.reference,t.person,t.remarks FROM transactions t JOIN inventory i ON i.id=t.item_id ORDER BY t.id DESC LIMIT 200""",con)
    st.dataframe(tx,use_container_width=True,hide_index=True)

# ---------- Production ----------
elif menu == "Production & Job Cards":
    header("Production & Job Cards", "Daily production entry with operator and job-card traceability")
    with st.form("production"):
        a,b,c,d1 = st.columns(4)
        pdate=a.date_input("Production Date",date.today())
        job=b.text_input("Job Card No.")
        product=c.text_input("Product")
        qty=d1.number_input("Production Qty",min_value=0.0)
        a,b,c=st.columns(3)
        unit=a.text_input("Unit","Pcs")
        operator=b.text_input("Operator")
        remarks=c.text_input("Remarks")
        if st.form_submit_button("Save Production",type="primary") and product:
            con.execute("""INSERT INTO production (prod_date,job_no,product,qty,unit,operator,remarks) VALUES(?,?,?,?,?,?,?)""",(str(pdate),job,product,qty,unit,operator,remarks))
            con.commit()
            st.success("Production entry saved.")
    p=pd.read_sql_query("SELECT * FROM production ORDER BY id DESC",con)
    st.dataframe(p,use_container_width=True,hide_index=True)

# ---------- Procurement ----------
elif menu == "Procurement":
    header("Procurement Control", "Automatic reorder identification and purchase requirement")
    if len(low):
        low2=low.copy()
        low2["Suggested Order"]=(low2.reorder_level*2-low2.qty).clip(lower=0)
        st.markdown(f'<div class="alert">âš  {len(low2)} item(s) require procurement action.</div>',unsafe_allow_html=True)
        st.dataframe(low2[["category","item_name","specification","qty","unit","reorder_level","Suggested Order","lot_no"]],
                     use_container_width=True,hide_index=True)
        st.download_button("Export Purchase Requirement",low2.to_csv(index=False).encode(),"purchase_requirement.csv","text/csv")
    else:
        st.markdown('<div class="good">âœ“ No procurement alerts.</div>',unsafe_allow_html=True)

    with st.expander("ï¼‹ Create Purchase Requirement"):
        with st.form("po"):
            a,b,c,d1=st.columns(4)
            po_date=a.date_input("Date",date.today())
            vendor=b.text_input("Vendor")
            item=b.text_input("Item")
            qty=c.number_input("Qty",min_value=0.0)
            unit=d1.text_input("Unit","Pcs")
            status=st.selectbox("Status",["DRAFT","SENT","RECEIVED"])
            ref=st.text_input("PO / Reference")
            remarks=st.text_input("Remarks")
            if st.form_submit_button("Save Procurement Record",type="primary") and item:
                con.execute("""INSERT INTO purchase_orders (po_date,vendor,item,qty,unit,status,reference,remarks) VALUES(?,?,?,?,?,?,?,?)""",(str(po_date),vendor,item,qty,unit,status,ref,remarks))
                con.commit()
                st.success("Procurement record saved.")

    po=pd.read_sql_query("SELECT * FROM purchase_orders ORDER BY id DESC",con)
    if len(po): st.dataframe(po,use_container_width=True,hide_index=True)

# ---------- MIS ----------
else:
    header("MIS Reports", "Management information system reports for daily review and control")
    t1,t2,t3,t4=st.tabs(["Stock MIS","Transaction MIS","Production MIS","Procurement MIS"])
    with t1:
        st.dataframe(d[["category","item_name","specification","qty","unit","reorder_level","lot_no"]],use_container_width=True,hide_index=True)
        st.download_button("Download Stock MIS",d.to_csv(index=False).encode(),"stock_mis.csv","text/csv")
    with t2:
        tx=pd.read_sql_query("""SELECT t.trans_date,t.trans_type,i.category,i.item_name, i.specification,t.qty,i.unit,t.reference,t.person,t.remarks FROM transactions t JOIN inventory i ON i.id=t.item_id ORDER BY t.id DESC""",con)
        st.dataframe(tx,use_container_width=True,hide_index=True)
        st.download_button("Download Transaction MIS",tx.to_csv(index=False).encode(),"transaction_mis.csv","text/csv")
    with t3:
        p=pd.read_sql_query("SELECT * FROM production ORDER BY id DESC",con)
        st.dataframe(p,use_container_width=True,hide_index=True)
        st.download_button("Download Production MIS",p.to_csv(index=False).encode(),"production_mis.csv","text/csv")
    with t4:
        po=pd.read_sql_query("SELECT * FROM purchase_orders ORDER BY id DESC",con)
        st.dataframe(po,use_container_width=True,hide_index=True)
        st.download_button("Download Procurement MIS",po.to_csv(index=False).encode(),"procurement_mis.csv","text/csv")
