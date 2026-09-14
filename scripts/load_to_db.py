import csv
import sqlite3

conn = sqlite3.connect('data/bank_churn.db')
cursor = conn.cursor()

with open('data/bank_churn.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    
    cursor.execute('DROP TABLE IF EXISTS bank_churn')
    columns = ', '.join([f'"{h}" TEXT' for h in headers])
    cursor.execute(f'CREATE TABLE bank_churn ({columns})')
    
    placeholders = ', '.join(['?'] * len(headers))
    cursor.executemany(f'INSERT INTO bank_churn VALUES ({placeholders})', reader)

conn.commit()
conn.close()

print("Baza danych data/bank_churn.db została pomyślnie utworzona!")