
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

APP_DIR = Path(__file__).resolve().parent
DB = APP_DIR / "erp.db"
OPENING = APP_DIR / "opening_inventory.csv"

st.set_page_config(page_title="RAI FACTORY ERP", page_icon="📦", layout="wide")

def db():
    con = sqlite3.connect(DB)
    con.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        item_name TEXT,
        specification TEXT,
        unit TEXT,
        qty REAL DEFAULT 0,
        reorder_level REAL DEFAULT 0,
        lot_no TEXT DEFAULT '',
        updated_at TEXT
    )""")
    con.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trans_date TEXT,
        trans_type TEXT,
        item_id INTEGER,
        qty REAL,
        reference TEXT,
        person TEXT,
        remarks TEXT
    )""")
    con.execute("""
    CREATE TABLE IF NOT EXISTS production(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prod_date TEXT,
        job_no TEXT,
        product TEXT,
        qty REAL,
        unit TEXT,
        operator TEXT,
        remarks TEXT
    )""")
    con.commit()
    return con

def seed():
    con = db()
    n = con.execute("SELECT COUNT(*) FROM inventory").fetchone()[0]
    if n == 0 and OPENING.exists():
        d = pd.read_csv(OPENING).fillna("")
        for _, r in d.iterrows():
            con.execute("""INSERT INTO inventory
                (category,item_name,specification,unit,qty,reorder_level,updated_at)
                VALUES(?,?,?,?,?,?,?)""",
                (r["category"],r["item_name"],r["specification"],r["unit"],
                 float(r["opening_qty"]),float(r["reorder_level"]),datetime.now().isoformat()))
        con.commit()
    return con

con = seed()

st.title("📦 RAI FACTORY ERP")
st.caption("Inventory • Procurement • Production • Stock Issue/Receipt • MIS")

menu = st.sidebar.radio("MENU", [
    "Dashboard","Inventory","Stock Issue / Receipt","Production","Procurement / Reorder","Reports"
])

def inventory_df():
    return pd.read_sql_query("SELECT * FROM inventory ORDER BY category, item_name", con)

if menu == "Dashboard":
    d = inventory_df()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Items", len(d))
    c2.metric("Total Categories", d["category"].nunique() if len(d) else 0)
    low = d[(d["reorder_level"] > 0) & (d["qty"] <= d["reorder_level"])]
    c3.metric("Low Stock", len(low))
    c4.metric("Zero Stock", int((d["qty"] <= 0).sum()))
    st.subheader("Low Stock")
    if len(low):
        st.dataframe(low[["category","item_name","specification","qty","unit","reorder_level","lot_no"]],
                     use_container_width=True, hide_index=True)
    else:
        st.success("No low-stock items based on current reorder levels.")
    st.subheader("Stock by Category")
    if len(d):
        st.bar_chart(d.groupby("category")["qty"].sum())

elif menu == "Inventory":
    st.subheader("Inventory Master")
    d = inventory_df()
    search = st.text_input("Search item / specification")
    cat = st.selectbox("Category", ["All"] + sorted(d["category"].dropna().unique().tolist()))
    view = d.copy()
    if search:
        mask = view.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False))
        view = view[mask.any(axis=1)]
    if cat != "All":
        view = view[view["category"] == cat]
    st.dataframe(view[["id","category","item_name","specification","unit","qty","reorder_level","lot_no","updated_at"]],
                 use_container_width=True, hide_index=True)
    st.download_button("Download Inventory CSV", view.to_csv(index=False).encode(),
                       "inventory.csv","text/csv")

    st.divider()
    st.subheader("Add / Update Item")
    with st.form("item_form"):
        a,b,c = st.columns(3)
        category = a.text_input("Category")
        item = b.text_input("Item Name")
        spec = c.text_input("Specification")
        d1,d2,d3 = st.columns(3)
        unit = d1.text_input("Unit", value="Pcs")
        qty = d2.number_input("Opening / Current Qty", min_value=0.0, value=0.0)
        reorder = d3.number_input("Reorder Level", min_value=0.0, value=0.0)
        lot = st.text_input("Lot No.")
        submitted = st.form_submit_button("Save Item")
        if submitted and item:
            con.execute("""INSERT INTO inventory
                (category,item_name,specification,unit,qty,reorder_level,lot_no,updated_at)
                VALUES(?,?,?,?,?,?,?,?)""",
                (category,item,spec,unit,qty,reorder,lot,datetime.now().isoformat()))
            con.commit()
            st.success("Item saved. Refresh to see it in the master.")

elif menu == "Stock Issue / Receipt":
    st.subheader("Stock Transaction")
    d = inventory_df()
    if len(d) == 0:
        st.warning("No inventory items.")
    else:
        labels = {f'{r.id} | {r.item_name} | {r.specification}': r.id for r in d.itertuples()}
        choice = st.selectbox("Item", list(labels.keys()))
        item_id = labels[choice]
        row = d[d.id == item_id].iloc[0]
        st.info(f"Current stock: {row.qty:g} {row.unit}")
        with st.form("txn"):
            typ = st.selectbox("Transaction", ["RECEIPT","ISSUE","ADJUSTMENT"])
            q = st.number_input("Quantity", min_value=0.0, value=1.0)
            ref = st.text_input("Reference / Job Card No.")
            person = st.text_input("Issued/Received By")
            remarks = st.text_input("Remarks")
            ok = st.form_submit_button("Post Transaction")
            if ok:
                delta = q if typ == "RECEIPT" else (-q if typ == "ISSUE" else q-row.qty)
                newqty = row.qty + delta
                if newqty < 0:
                    st.error("Insufficient stock.")
                else:
                    con.execute("UPDATE inventory SET qty=?,updated_at=? WHERE id=?",
                                (newqty,datetime.now().isoformat(),item_id))
                    con.execute("""INSERT INTO transactions
                        (trans_date,trans_type,item_id,qty,reference,person,remarks)
                        VALUES(?,?,?,?,?,?,?)""",
                        (datetime.now().strftime("%Y-%m-%d %H:%M"),typ,item_id,q,ref,person,remarks))
                    con.commit()
                    st.success(f"Posted. New stock: {newqty:g} {row.unit}")

    st.subheader("Recent Transactions")
    tx = pd.read_sql_query("""
        SELECT t.trans_date,t.trans_type,i.item_name,i.specification,
               t.qty,i.unit,t.reference,t.person,t.remarks
        FROM transactions t JOIN inventory i ON i.id=t.item_id
        ORDER BY t.id DESC LIMIT 100
    """, con)
    st.dataframe(tx, use_container_width=True, hide_index=True)

elif menu == "Production":
    st.subheader("Production / Job Card")
    with st.form("production"):
        a,b,c = st.columns(3)
        pdate = a.date_input("Production Date", datetime.now().date())
        job = b.text_input("Job Card No.")
        product = c.text_input("Product")
        d1,d2,d3 = st.columns(3)
        qty = d1.number_input("Production Qty", min_value=0.0, value=0.0)
        unit = d2.text_input("Unit", value="Pcs")
        operator = d3.text_input("Operator")
        remarks = st.text_input("Remarks")
        ok = st.form_submit_button("Save Production")
        if ok and product:
            con.execute("""INSERT INTO production
                (prod_date,job_no,product,qty,unit,operator,remarks)
                VALUES(?,?,?,?,?,?,?)""",
                (str(pdate),job,product,qty,unit,operator,remarks))
            con.commit()
            st.success("Production entry saved.")

    p = pd.read_sql_query("SELECT * FROM production ORDER BY id DESC", con)
    st.dataframe(p, use_container_width=True, hide_index=True)

elif menu == "Procurement / Reorder":
    st.subheader("Reorder / Procurement")
    d = inventory_df()
    low = d[(d["reorder_level"] > 0) & (d["qty"] <= d["reorder_level"])].copy()
    if len(low):
        low["suggested_order"] = (low["reorder_level"] * 2 - low["qty"]).clip(lower=0)
        st.dataframe(low[["category","item_name","specification","qty","unit","reorder_level","suggested_order","lot_no"]],
                     use_container_width=True, hide_index=True)
        st.download_button("Download Purchase Requirement", low.to_csv(index=False).encode(),
                           "purchase_requirement.csv","text/csv")
    else:
        st.success("No items are currently below their reorder levels.")
    st.caption("Set reorder levels from Inventory → Add / Update Item. The ERP then creates the procurement list automatically.")

elif menu == "Reports":
    st.subheader("MIS Reports")
    d = inventory_df()
    tab1,tab2 = st.tabs(["Stock Report","Transaction Report"])
    with tab1:
        st.dataframe(d[["category","item_name","specification","qty","unit","reorder_level","lot_no"]],
                     use_container_width=True, hide_index=True)
        st.download_button("Export Stock MIS", d.to_csv(index=False).encode(),
                           "stock_mis.csv","text/csv")
    with tab2:
        tx = pd.read_sql_query("""
            SELECT t.trans_date,t.trans_type,i.category,i.item_name,i.specification,
                   t.qty,i.unit,t.reference,t.person,t.remarks
            FROM transactions t JOIN inventory i ON i.id=t.item_id
            ORDER BY t.id DESC
        """, con)
        st.dataframe(tx, use_container_width=True, hide_index=True)
        st.download_button("Export Transaction MIS", tx.to_csv(index=False).encode(),
                           "transaction_mis.csv","text/csv")

st.sidebar.divider()
st.sidebar.caption("Starting inventory imported from Ayka stock workbook.")
