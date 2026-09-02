import os
import sys
import pandas as pd
import customtkinter as ctk
from tkinter import ttk, messagebox


def get_excel_path():
    """
    Always look for Ayka stock.xlsx beside the EXE.
    During Python development, look beside app.py.
    """
    if getattr(sys, "frozen", False):
        app_folder = os.path.dirname(sys.executable)
    else:
        app_folder = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(app_folder, "Ayka stock.xlsx")


EXCEL_FILE = get_excel_path()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AYKAERP:

    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("AYKA ERP SOFTWARE")
        self.app.geometry("1400x800")
        self.current_data = pd.DataFrame()

        ctk.CTkLabel(
            self.app,
            text="AYKA ERP SOFTWARE",
            font=("Arial", 30, "bold")
        ).pack(pady=(15, 0))

        ctk.CTkLabel(
            self.app,
            text="RAW MATERIAL STOCK MANAGEMENT SYSTEM",
            font=("Arial", 16)
        ).pack(pady=(0, 12))

        menu = ctk.CTkFrame(self.app)
        menu.pack(fill="x", padx=15, pady=8)

        buttons = [
            ("All Stock", self.all_stock),
            ("Paper Roll", lambda: self.section("B:F", 6, 35)),
            ("Poly Inventory", lambda: self.section("H:J", 6, 35)),
            ("Ink Stock", lambda: self.section("M:O", 6, 35)),
            ("Paper Sheet", lambda: self.section("B:F", 39, 25)),
            ("Box Inventory", lambda: self.section("H:J", 39, 25)),
            ("Core Inventory", lambda: self.section("M:O", 39, 25)),
            ("Low Stock", self.low_stock),
        ]

        for text, command in buttons:
            ctk.CTkButton(
                menu,
                text=text,
                command=command,
                width=140
            ).pack(side="left", padx=4, pady=8)

        search_frame = ctk.CTkFrame(self.app)
        search_frame.pack(fill="x", padx=15, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search Material Name..."
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=8
        )

        ctk.CTkButton(
            search_frame,
            text="SEARCH",
            command=self.search_material
        ).pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(self.app)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree = ttk.Treeview(table_frame)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar_y.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.status = ctk.CTkLabel(
            self.app,
            text="Ready"
        )
        self.status.pack(pady=5)

        self.all_stock()
        self.app.mainloop()

    def read_excel(self, **kwargs):
        if not os.path.exists(EXCEL_FILE):
            messagebox.showerror(
                "Excel File Not Found",
                "Ayka stock.xlsx was not found.\n\n"
                "Please keep this file in the SAME folder as app.exe.\n\n"
                f"Expected location:\n{EXCEL_FILE}"
            )
            return pd.DataFrame()

        try:
            df = pd.read_excel(
                EXCEL_FILE,
                sheet_name=0,
                **kwargs
            )
            return df.dropna(how="all")

        except Exception as e:
            messagebox.showerror(
                "Excel Error",
                f"Could not read Excel file:\n\n{e}"
            )
            return pd.DataFrame()

    def show_data(self, df):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if df.empty:
            self.tree["columns"] = []
            self.status.configure(text="No data found")
            return

        columns = [str(col) for col in df.columns]
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=170, anchor="center")

        for _, row in df.iterrows():
            values = [
                "" if pd.isna(value) else str(value)
                for value in row.tolist()
            ]
            self.tree.insert("", "end", values=values)

        self.current_data = df
        self.status.configure(
            text=f"Excel: {os.path.basename(EXCEL_FILE)} | Total Records: {len(df)}"
        )

    def all_stock(self):
        df = self.read_excel(header=None)
        self.show_data(df)

    def section(self, usecols, skiprows, nrows):
        df = self.read_excel(
            usecols=usecols,
            skiprows=skiprows,
            nrows=nrows
        )
        self.show_data(df)

    def search_material(self):
        search_text = self.search_entry.get().strip().lower()

        if not search_text:
            return

        if self.current_data.empty:
            return

        mask = self.current_data.astype(str).apply(
            lambda row: row.str.lower().str.contains(
                search_text,
                na=False
            ).any(),
            axis=1
        )

        self.show_data(self.current_data[mask])

    def low_stock(self):
        df = self.read_excel(header=None)

        if df.empty:
            return

        result_rows = []

        for _, row in df.iterrows():
            numeric_values = []

            for value in row:
                try:
                    numeric_values.append(float(value))
                except Exception:
                    pass

            if numeric_values and any(0 <= x < 10 for x in numeric_values):
                result_rows.append(row.tolist())

        result = pd.DataFrame(result_rows)
        self.show_data(result)


if __name__ == "__main__":
    AYKAERP()
