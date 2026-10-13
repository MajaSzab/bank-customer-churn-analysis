import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11})

# 1. Load data from SQLite database
conn = sqlite3.connect('data/bank_churn.db')
df = pd.read_sql_query("SELECT Age, NumOfProducts, Exited, Geography FROM bank_churn;", conn)
conn.close()

# Convert numeric columns
for col in ['Age', 'NumOfProducts', 'Exited']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Create a figure with 2 subplots side-by-side
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Chart 1: Churn Rate by Number of Products (Business Anomaly)
product_churn = df.groupby('NumOfProducts')['Exited'].mean().reset_index()
product_churn['ChurnRate_Pct'] = product_churn['Exited'] * 100

sns.barplot(
    data=product_churn, 
    x='NumOfProducts', 
    y='ChurnRate_Pct', 
    ax=axes[0], 
    palette='Reds_d'
)
axes[0].set_title('Churn Rate (%) by Number of Products', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Number of Products', fontsize=12)
axes[0].set_ylabel('Churn Rate (%)', fontsize=12)
axes[0].set_ylim(0, 100)

# Add values above bars
for bar in axes[0].patches:
    axes[0].annotate(f"{bar.get_height():.1f}%",
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        ha='center', va='bottom', fontsize=11, xytext=(0, 3),
                        textcoords='offset points')

# Chart 2: Age Distribution by Churn Status
sns.kdeplot(
    data=df, 
    x='Age', 
    hue='Exited', 
    common_norm=False, 
    fill=True, 
    palette=['#2b5c8f', '#d9534f'], 
    ax=axes[1]
)
axes[1].set_title('Age Distribution: Stayed vs Churned', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Age', fontsize=12)
axes[1].set_ylabel('Density', fontsize=12)
axes[1].legend(title='Customer Status', labels=['Churned (1)', 'Stayed (0)'])

plt.tight_layout()

# 2. Save charts to the reports/ directory
plt.savefig('reports/churn_analysis_charts.png', dpi=300)
print("Chart image successfully saved to reports/churn_analysis_charts.png!")