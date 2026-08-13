import sqlite3
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
