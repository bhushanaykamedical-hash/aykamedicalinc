import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime, date

APP = Path(__file__).parent
DB = APP / "rai_factory_erp.db"
OPENING = APP / "opening_inventory.csv"

st.set_page_config(
    page_title="RAI Factory ERP",
    page_icon="ðŸ“¦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Professional UI ----------
st.markdown(""" <style> .stApp {background:#f4f6f9;} [data-testid="stSidebar"] {background:#10233f;} [data-testid="stSidebar"] * {color:#eef5ff !important;} .block-container {max-width:1500px;padding-top:1.1rem;} .brand {font-size:25px;font-weight:800;color:white;letter-spacing:.4px;} .brand2 {font-size:11px;color:#9db6d6;margin-top:-3px;letter-spacing:1.2px;} .topbar {background:white;border:1px solid #e5e9ef;border-radius:14px;padding:18px 22px;margin-bottom:16px;} .title {font-size:29px;font-weight:800;color:#10233f;} .sub {font-size:13px;color:#667085;margin-top:2px;} .kpi {background:white;border:1px solid #e4e8ee;border-radius:14px;padding:17px 19px;box-shadow:0 2px 10px rgba(16,35,63,.05);} .kpi-label {font-size:11px;font-weight:700;color:#667085;text-transform:uppercase;letter-spacing:.6px;} .kpi-value {font-size:28px;font-weight:800;color:#10233f;margin-top:4px;} .kpi-note {font-size:11px;color:#98a2b3;margin-top:2px;} .section {font-size:18px;font-weight:800;color:#10233f;margin:22px 0 10px;} .alert {background:#fff4f2;border:1px solid #ffd6d1;color:#b42318;border-radius:12px;padding:12px 14px;font-weight:650;} .good {background:#ecfdf3;border:1px solid #abefc6;color:#067647;border-radius:12px;padding:12px 14px;font-weight:650;} .stButton>button {border-radius:9px;font-weight:650;} div[data-testid="stMetric"] {background:white;border:1px solid #e4e8ee;border-radius:12px;} </style> """, unsafe_allow_html=True)

# ---------- DB ----------
def db():
    con = sqlite3.connect(DB, check_same_thread=False)
    con.execute("""CREATE TABLE IF NOT EXISTS inventory( id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, item_name TEXT, specification TEXT, unit TEXT, qty REAL DEFAULT 0, reorder_level REAL DEFAULT 0, lot_no TEXT DEFAULT '', updated_at TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS transactions( id INTEGER PRIMARY KEY AUTOINCREMENT, trans_date TEXT, trans_type TEXT, item_id INTEGER, qty REAL, reference TEXT, person TEXT, remarks TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS production( id INTEGER PRIMARY KEY AUTOINCREMENT, prod_date TEXT, job_no TEXT, product TEXT, qty REAL, unit TEXT, operator TEXT, remarks TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS purchase_orders( id INTEGER PRIMARY KEY AUTOINCREMENT, po_date TEXT, vendor TEXT, item TEXT, qty REAL, unit TEXT, status TEXT, reference TEXT, remarks TEXT)""")
    con.commit()
    return con

con = db()

if con.execute("SELECT COUNT(*) FROM inventory").fetchone()[0] == 0 and OPENING.exists():
    x = pd.read_csv(OPENING).fillna("")
    for _, r in x.iterrows():
        con.execute("""INSERT INTO inventory (category,item_name,specification,unit,qty,reorder_level,lot_no,updated_at) VALUES(?,?,?,?,?,?,?,?)""",
        (r.category,r.item_name,r.specification,r.unit,float(r.opening_qty),
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
