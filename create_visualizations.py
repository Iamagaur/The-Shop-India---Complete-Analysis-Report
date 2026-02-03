"""
THE SHOP INDIA - DATA VISUALIZATIONS
=====================================
Creates professional charts for analysis presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Load data
df = pd.read_csv('product_analysis_data.csv')

print("Creating visualizations...")

# ============================================================================
# CHART 1: Revenue by Category
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

category_revenue = df.groupby('Main_Category')['Revenue_30_Days'].sum().sort_values(ascending=False)

colors = plt.cm.Set3(np.linspace(0, 1, len(category_revenue)))
bars = ax.barh(category_revenue.index, category_revenue.values / 1000000, color=colors)

# Add value labels
for i, (idx, val) in enumerate(category_revenue.items()):
    ax.text(val/1000000 + 0.5, i, f'₹{val/1000000:.1f}M', 
            va='center', fontweight='bold')

ax.set_xlabel('Revenue (Million ₹)', fontsize=12, fontweight='bold')
ax.set_title('The Shop India - Category Revenue Performance (Last 30 Days)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('chart1_category_revenue.png', dpi=300, bbox_inches='tight')
print("✓ Created: chart1_category_revenue.png")
plt.close()

# ============================================================================
# CHART 2: Price Distribution
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Price histogram
ax1.hist(df['Price_INR'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
ax1.axvline(df['Price_INR'].median(), color='red', linestyle='--', 
            linewidth=2, label=f'Median: ₹{df["Price_INR"].median():.0f}')
ax1.axvline(df['Price_INR'].mean(), color='green', linestyle='--', 
            linewidth=2, label=f'Mean: ₹{df["Price_INR"].mean():.0f}')
ax1.set_xlabel('Price (₹)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Number of Products', fontsize=11, fontweight='bold')
ax1.set_title('Price Distribution', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Box plot by category
df.boxplot(column='Price_INR', by='Main_Category', ax=ax2)
ax2.set_xlabel('Category', fontsize=11, fontweight='bold')
ax2.set_ylabel('Price (₹)', fontsize=11, fontweight='bold')
ax2.set_title('Price Range by Category', fontsize=12, fontweight='bold')
plt.sca(ax2)
plt.xticks(rotation=45, ha='right')

plt.suptitle('The Shop India - Pricing Analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('chart2_price_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Created: chart2_price_analysis.png")
plt.close()

# ============================================================================
# CHART 3: Best Sellers by Category
# ============================================================================

fig, ax = plt.subplots(figsize=(14, 8))

# Get top 3 from each category
top_products = []
for category in df['Main_Category'].unique():
    cat_top = df[df['Main_Category'] == category].nlargest(3, 'Units_Sold_30_Days')
    top_products.append(cat_top)

top_df = pd.concat(top_products)
top_df = top_df.sort_values(['Main_Category', 'Units_Sold_30_Days'], ascending=[True, False])

# Create grouped bar chart
categories = top_df['Main_Category'].unique()
x = np.arange(len(categories))
width = 0.25

for i in range(3):
    values = []
    for cat in categories:
        cat_data = top_df[top_df['Main_Category'] == cat]
        if len(cat_data) > i:
            values.append(cat_data.iloc[i]['Units_Sold_30_Days'])
        else:
            values.append(0)
    
    ax.bar(x + i*width, values, width, label=f'#{i+1} Bestseller', alpha=0.8)

ax.set_ylabel('Units Sold (30 Days)', fontsize=12, fontweight='bold')
ax.set_title('Top 3 Best-Selling Products per Category', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x + width)
ax.set_xticklabels(categories, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('chart3_bestsellers.png', dpi=300, bbox_inches='tight')
print("✓ Created: chart3_bestsellers.png")
plt.close()

# ============================================================================
# CHART 4: Stock Status Analysis
# ============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Overall stock status pie chart
stock_counts = df['Stock_Status'].value_counts()
colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
ax1.pie(stock_counts.values, labels=stock_counts.index, autopct='%1.1f%%',
        colors=colors_pie, startangle=90)
ax1.set_title('Overall Stock Status', fontsize=12, fontweight='bold')

# Stock status by category
stock_by_cat = pd.crosstab(df['Main_Category'], df['Stock_Status'])
stock_by_cat.plot(kind='bar', stacked=True, ax=ax2, color=colors_pie, alpha=0.8)
ax2.set_xlabel('Category', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Products', fontsize=11, fontweight='bold')
ax2.set_title('Stock Status by Category', fontsize=12, fontweight='bold')
ax2.legend(title='Status')
plt.sca(ax2)
plt.xticks(rotation=45, ha='right')

plt.suptitle('The Shop India - Inventory Analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('chart4_stock_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Created: chart4_stock_analysis.png")
plt.close()

# ============================================================================
# CHART 5: Customer Ratings
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

rating_by_cat = df.groupby('Main_Category')['Customer_Rating'].mean().sort_values(ascending=False)

colors_ratings = ['#27ae60' if x >= 4.2 else '#f39c12' if x >= 4.0 else '#e74c3c' 
                  for x in rating_by_cat.values]

bars = ax.barh(rating_by_cat.index, rating_by_cat.values, color=colors_ratings)

# Add value labels
for i, (idx, val) in enumerate(rating_by_cat.items()):
    ax.text(val + 0.01, i, f'{val:.2f}', va='center', fontweight='bold')

# Add benchmark line
ax.axvline(4.0, color='red', linestyle='--', linewidth=2, label='Benchmark (4.0)', alpha=0.5)
ax.axvline(df['Customer_Rating'].mean(), color='blue', linestyle='--', 
           linewidth=2, label=f'Average ({df["Customer_Rating"].mean():.2f})', alpha=0.5)

ax.set_xlabel('Average Customer Rating', fontsize=12, fontweight='bold')
ax.set_title('Customer Satisfaction by Category', fontsize=14, fontweight='bold', pad=20)
ax.set_xlim(3.5, 5.0)
ax.legend()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('chart5_customer_ratings.png', dpi=300, bbox_inches='tight')
print("✓ Created: chart5_customer_ratings.png")
plt.close()

# ============================================================================
# CHART 6: Performance Matrix (Revenue vs Units)
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 8))

category_data = df.groupby('Main_Category').agg({
    'Revenue_30_Days': 'sum',
    'Units_Sold_30_Days': 'sum',
    'Customer_Rating': 'mean'
}).reset_index()

# Scatter plot
scatter = ax.scatter(category_data['Units_Sold_30_Days'], 
                    category_data['Revenue_30_Days'] / 1000000,
                    s=category_data['Customer_Rating'] * 200,
                    c=range(len(category_data)),
                    cmap='viridis',
                    alpha=0.6,
                    edgecolors='black',
                    linewidth=2)

# Add labels
for idx, row in category_data.iterrows():
    ax.annotate(row['Main_Category'], 
                (row['Units_Sold_30_Days'], row['Revenue_30_Days']/1000000),
                xytext=(5, 5), textcoords='offset points',
                fontweight='bold', fontsize=10)

ax.set_xlabel('Total Units Sold (30 Days)', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Revenue (Million ₹)', fontsize=12, fontweight='bold')
ax.set_title('Category Performance Matrix\n(Bubble Size = Customer Rating)', 
             fontsize=14, fontweight='bold', pad=20)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('chart6_performance_matrix.png', dpi=300, bbox_inches='tight')
print("✓ Created: chart6_performance_matrix.png")
plt.close()

print("\n✅ All visualizations created successfully!")
print("\nGenerated Charts:")
print("  1. chart1_category_revenue.png - Revenue by category")
print("  2. chart2_price_analysis.png - Price distribution analysis")
print("  3. chart3_bestsellers.png - Best sellers comparison")
print("  4. chart4_stock_analysis.png - Inventory status")
print("  5. chart5_customer_ratings.png - Customer satisfaction")
print("  6. chart6_performance_matrix.png - Performance matrix")
