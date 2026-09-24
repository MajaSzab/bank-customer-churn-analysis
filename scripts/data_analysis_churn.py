import sqlite3
import pandas as pd

#Połączenie z bazą SQLite i wczytanie danych
conn = sqlite3.connect('data/bank_churn.db')
query = "SELECT * FROM bank_churn;"
df = pd.read_sql_query(query, conn)
conn.close()

#Konwersja typów danych 
numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Analiza danych: Podstawowe statystyki i brakujące wartości 
print("PODSUMOWANIE ZBIORU DANYCH")
print(f"Liczba wierszy: {df.shape[0]}, Liczba kolumn: {df.shape[1]}\n")

print("BRAKI DANYCH")
print(df.isnull().sum(), "\n")

print("STATYSTYKI OPISOWE")
print(df[['CreditScore', 'Age', 'Balance', 'EstimatedSalary']].describe().round(2), "\n")

#Analiza biznesowa: Wpływ liczby produktów na Churn Rate
product_churn = df.groupby('NumOfProducts')['Exited'].agg(
    total_customers='count',
    churned_customers='sum',
    churn_rate_pct=lambda x: round(x.mean() * 100, 2)
).reset_index()

print("CHURN RATE WG LICZBY PRODUKTÓW")
print(product_churn, "\n")

#Zapis wyników zagregowanych do pliku CSV
product_churn.to_csv('data/churn_by_products.csv', index=False)
print("Plik data/churn_by_products.csv został pomyślnie wygenerowany!")