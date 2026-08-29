import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3,hashlib
from datetime import date
DB="manufacturing_erp.db"
def hp(p): return hashlib.sha256(p.encode()).hexdigest()

class App:
 def __init__(self,root):
  self.r=root; self.c=sqlite3.connect(DB); self.setup(); self.login()
 def setup(self):
  q=["CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE,password TEXT,name TEXT,role TEXT)",
     "CREATE TABLE IF NOT EXISTS products(code TEXT UNIQUE,name TEXT,unit TEXT,min_stock REAL)",
     "CREATE TABLE IF NOT EXISTS materials(code TEXT UNIQUE,name TEXT,unit TEXT,min_stock REAL)",
     "CREATE TABLE IF NOT EXISTS bom(product TEXT,material TEXT,consumption REAL)",
     "CREATE TABLE IF NOT EXISTS orders(fo TEXT UNIQUE,dt TEXT,product TEXT,qty REAL,produced REAL DEFAULT 0,status TEXT DEFAULT 'Running')",
     "CREATE TABLE IF NOT EXISTS purchase(dt TEXT,material TEXT,qty REAL,supplier TEXT)",
     "CREATE TABLE IF NOT EXISTS issue(dt TEXT,fo TEXT,material TEXT,qty REAL)",
     "CREATE TABLE IF NOT EXISTS production(dt TEXT,fo TEXT,product TEXT,good REAL,reject REAL)"]
  for x in q:self.c.execute(x)
  if self.c.execute("SELECT COUNT(*) FROM users").fetchone()[0]==0:
   self.c.execute("INSERT INTO users(username,password,name,role) VALUES(?,?,?,?)",("admin",hp("admin123"),"System Administrator","Admin"))
  self.c.commit()
 def login(self):
  self.r.title("Manufacturing ERP - Login"); self.r.geometry("400x300")
  f=ttk.Frame(self.r,padding=30);f.pack(fill="both",expand=True)
  ttk.Label(f,text="MANUFACTURING ERP",font=("Arial",20,"bold")).pack(pady=10)
  ttk.Label(f,text="Username").pack(anchor="w");self.u=ttk.Entry(f);self.u.pack(fill="x",pady=5)
  ttk.Label(f,text="Password").pack(anchor="w");self.p=ttk.Entry(f,show="*");self.p.pack(fill="x",pady=5)
  ttk.Button(f,text="LOGIN",command=self.check).pack(fill="x",pady=15)
  ttk.Label(f,text="Default: admin / admin123").pack()
  self.r.bind("<Return>",lambda e:self.check())
 def check(self):
  row=self.c.execute("SELECT username,name,role FROM users WHERE username=? AND password=?",(self.u.get(),hp(self.p.get()))).fetchone()
  if not row:return messagebox.showerror("Login Failed","Invalid username or password")
  self.user,self.name,self.role=row
  for w in self.r.winfo_children():w.destroy()
  self.main()
 def main(self):
  self.r.title(f"Manufacturing ERP - {self.name} ({self.role})");self.r.geometry("1200x700")
  top=ttk.Frame(self.r,padding=8);top.pack(fill="x")
  ttk.Label(top,text="MANUFACTURING ERP SOFTWARE",font=("Arial",18,"bold")).pack(side="left")
  ttk.Label(top,text=f"Logged in: {self.name} | {self.role}").pack(side="right")
  self.nb=ttk.Notebook(self.r);self.nb.pack(fill="both",expand=True,padx=8,pady=8)
  for n in ["Dashboard","Products","Materials","BOM","Factory Orders","Purchase","Material Issue","Production","Stock Report"]+(["Users"] if self.role=="Admin" else []):
   f=ttk.Frame(self.nb,padding=10);self.nb.add(f,text=n);setattr(self,n.replace(" ","_"),f)
  self.dashboard();self.master(self.Products,"Product","products",["Code","Name","Unit","Minimum Stock"]);self.master(self.Materials,"Material","materials",["Code","Name","Unit","Minimum Stock"])
  self.simple(self.BOM,"BOM","bom",["Product Code","Material Code","Consumption per PCS"])
  self.simple(self.Factory_Orders,"Factory Order","orders",["FO No","Date","Product Code","Order Qty"])
  self.simple(self.Purchase,"Purchase Inward","purchase",["Date","Material Code","Qty","Supplier"])
  self.simple(self.Material_Issue,"Material Issue","issue",["Date","FO No","Material Code","Qty"])
  self.simple(self.Production,"Production","production",["Date","FO No","Product Code","Good Qty","Reject Qty"])
  self.stock()
  if self.role=="Admin":self.users()
 def dashboard(self):
  f=self.Dashboard
  labels=[("Products","SELECT COUNT(*) FROM products"),("Materials","SELECT COUNT(*) FROM materials"),("Orders","SELECT COUNT(*) FROM orders"),("Running Orders","SELECT COUNT(*) FROM orders WHERE status='Running'"),("Production","SELECT COALESCE(SUM(good),0) FROM production")]
  for i,(t,q) in enumerate(labels):
   b=ttk.LabelFrame(f,text=t,padding=25);b.grid(row=i//3,column=i%3,padx=10,pady=10,sticky="nsew")
   ttk.Label(b,text=str(self.c.execute(q).fetchone()[0]),font=("Arial",24,"bold")).pack()
 def master(self,f,title,table,labels):
  self.simple(f,title,table,labels)
 def simple(self,f,title,table,labels):
  form=ttk.LabelFrame(f,text=title,padding=8);form.pack(fill="x"); es=[]
  for i,l in enumerate(labels):
   ttk.Label(form,text=l).grid(row=0,column=i,padx=3);e=ttk.Entry(form,width=18);e.grid(row=1,column=i,padx=3);es.append(e)
  tree=ttk.Treeview(f,show="headings");tree.pack(fill="both",expand=True,pady=10)
  cols=["c"+str(i) for i in range(len(labels))];tree["columns"]=cols
  for c,l in zip(cols,labels):tree.heading(c,text=l);tree.column(c,width=150)
  def load():
   for x in tree.get_children():tree.delete(x)
   for row in self.c.execute("SELECT * FROM "+table):tree.insert("",'end',values=row[-len(labels):])
  def save():
   try:
    vals=[e.get() for e in es]
    if table=="products":self.c.execute("INSERT INTO products VALUES(?,?,?,?)",(vals[0],vals[1],vals[2],float(vals[3] or 0)))
    elif table=="materials":self.c.execute("INSERT INTO materials VALUES(?,?,?,?)",(vals[0],vals[1],vals[2],float(vals[3] or 0)))
    elif table=="bom":self.c.execute("INSERT INTO bom VALUES(?,?,?)",(vals[0],vals[1],float(vals[2] or 0)))
    elif table=="orders":self.c.execute("INSERT INTO orders(fo,dt,product,qty) VALUES(?,?,?,?)",(vals[0],vals[1] or str(date.today()),vals[2],float(vals[3] or 0)))
    elif table=="purchase":self.c.execute("INSERT INTO purchase VALUES(?,?,?,?)",(vals[0] or str(date.today()),vals[1],float(vals[2] or 0),vals[3]))
    elif table=="issue":self.c.execute("INSERT INTO issue VALUES(?,?,?,?)",(vals[0] or str(date.today()),vals[1],vals[2],float(vals[3] or 0)))
    elif table=="production":
     self.c.execute("INSERT INTO production VALUES(?,?,?,?,?)",(vals[0] or str(date.today()),vals[1],vals[2],float(vals[3] or 0),float(vals[4] or 0)))
     self.c.execute("UPDATE orders SET produced=produced+? WHERE fo=?",(float(vals[3] or 0),vals[1]))
     self.c.execute("UPDATE orders SET status='Completed' WHERE fo=? AND produced>=qty",(vals[1],))
    self.c.commit()
    for e in es:e.delete(0,'end')
    load()
   except Exception as x:messagebox.showerror("Error",str(x))
  ttk.Button(form,text="Save",command=save).grid(row=1,column=len(labels),padx=8);ttk.Button(form,text="Refresh",command=load).grid(row=1,column=len(labels)+1)
  load()
 def stock(self):
  f=self.Stock_Report
  tree=ttk.Treeview(f,columns=("code","inward","issued","closing","status"),show="headings")
  for c in tree["columns"]:tree.heading(c,text=c.title());tree.column(c,width=160)
  tree.pack(fill="both",expand=True)
  def load():
   for x in tree.get_children():tree.delete(x)
   for code,name,unit,mn in self.c.execute("SELECT * FROM materials"):
    inn=self.c.execute("SELECT COALESCE(SUM(qty),0) FROM purchase WHERE material=?",(code,)).fetchone()[0]
    out=self.c.execute("SELECT COALESCE(SUM(qty),0) FROM issue WHERE material=?",(code,)).fetchone()[0]
    cl=inn-out;tree.insert("",'end',values=(code,inn,out,cl,"LOW STOCK" if cl<mn else "OK"))
  ttk.Button(f,text="Refresh Stock Report",command=load).pack();load()
 def users(self):
  f=self.Users;form=ttk.Frame(f);form.pack(fill="x");es=[]
  for i,l in enumerate(["Username","Password","Full Name","Role"]):
   ttk.Label(form,text=l).grid(row=0,column=i);e=ttk.Entry(form);e.grid(row=1,column=i,padx=5);es.append(e)
  tree=ttk.Treeview(f,columns=("username","name","role"),show="headings")
  for c in tree["columns"]:tree.heading(c,text=c.title())
  tree.pack(fill="both",expand=True,pady=10)
  def load():
   for x in tree.get_children():tree.delete(x)
   for r in self.c.execute("SELECT username,name,role FROM users"):tree.insert("",'end',values=r)
  def add():
   try:
    role=es[3].get().title() if es[3].get().title() in ("Admin","User") else "User"
    self.c.execute("INSERT INTO users(username,password,name,role) VALUES(?,?,?,?)",(es[0].get(),hp(es[1].get()),es[2].get(),role));self.c.commit()
    [e.delete(0,'end') for e in es];load()
   except Exception as x:messagebox.showerror("Error",str(x))
  ttk.Button(form,text="Create User",command=add).grid(row=1,column=4,padx=8);load()

if __name__=="__main__":
 root=tk.Tk();App(root);root.mainloop()
