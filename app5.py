Dim fso, shell, desktopPath, dbPath, accessApp
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
