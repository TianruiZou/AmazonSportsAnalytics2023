#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set font for Chinese characters (if needed)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Create output directory
if not os.path.exists('output/visualization'):
    os.makedirs('output/visualization')

print('=' * 50)
print('Starting Data Visualization Analysis')
print('=' * 50)

# ==================== 1. Load cleaned data ====================
print('\n1. Loading cleaned data')
print('-' * 30)

try:
    df = pd.read_csv('output/amz_uk_further_cleaned.csv')
    print(f'Data successfully loaded, shape: {df.shape}')
except Exception as e:
    print(f'Error reading file: {e}')
    exit(1)

# ==================== A. Main category product count ====================
print('\nA. Product count by main category')
print('-' * 30)

main_category_counts = df['main_category'].value_counts().head(15)

plt.figure(figsize=(15, 8))
sns.barplot(x=main_category_counts.values, y=main_category_counts.index, palette='viridis')

for i, v in enumerate(main_category_counts.values):
    plt.text(v, i, f' {v:,}', va='center')

plt.title('Top 15 Main Category Product Counts', fontsize=14)
plt.xlabel('Product Count', fontsize=12)
plt.ylabel('Main Category', fontsize=12)
plt.tight_layout()
plt.savefig('output/visualization/main_category_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print('Main category product count chart generated')

# ==================== B. Product price distribution ====================
print('\nB. Product price distribution')
print('-' * 30)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

sns.histplot(data=df, x='price', bins=50, ax=ax1)
ax1.set_title('Product Price Histogram', fontsize=14)
ax1.set_xlabel('Price (£)', fontsize=12)
ax1.set_ylabel('Product Count', fontsize=12)

sns.boxplot(data=df, x='price', ax=ax2)
ax2.set_title('Product Price Boxplot', fontsize=14)
ax2.set_xlabel('Price (£)', fontsize=12)

plt.tight_layout()
plt.savefig('output/visualization/price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print('Price statistics:')
print(df['price'].describe())
print('Product price distribution charts generated')

# ==================== C. Star rating distribution ====================
print('\nC. Star rating distribution')
print('-' * 30)

plt.figure(figsize=(12, 6))
stars_counts = df['stars'].value_counts().sort_index()
sns.barplot(x=stars_counts.index, y=stars_counts.values, color='skyblue')

for i, v in enumerate(stars_counts.values):
    plt.text(i, v, f'{v:,}', ha='center', va='bottom')

plt.title('Star Rating Distribution', fontsize=14)
plt.xlabel('Star Rating', fontsize=12)
plt.ylabel('Product Count', fontsize=12)
plt.savefig('output/visualization/stars_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print('Star rating statistics:')
print(df['stars'].describe())
print('Star rating distribution chart generated')

# ==================== D. Review count distribution ====================
print('\nD. Review count distribution')
print('-' * 30)

plt.figure(figsize=(12, 6))
df_reviews = df[df['reviews'] <= 2000]
sns.histplot(data=df_reviews, x='reviews', bins=50)
plt.title('Review Count Distribution (≤ 2000)', fontsize=14)
plt.xlabel('Review Count', fontsize=12)
plt.ylabel('Product Count', fontsize=12)
plt.savefig('output/visualization/reviews_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print('Review count statistics:')
print(df['reviews'].describe())
print(f'Products with >2000 reviews: {len(df[df["reviews"] > 2000])}')
print('Review count distribution chart generated')

# ==================== E. BestSeller vs Non-BestSeller comparison ====================
print('\nE. BestSeller vs Non-BestSeller Comparison')
print('-' * 30)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

sns.boxplot(data=df, x='isBestSeller', y='stars', ax=axes[0])
axes[0].set_title('Star Rating Comparison', fontsize=12)
axes[0].set_xlabel('Best Seller', fontsize=10)
axes[0].set_ylabel('Star Rating', fontsize=10)
axes[0].set_xticklabels(['Non-BestSeller', 'BestSeller'])

sns.boxplot(data=df, x='isBestSeller', y='price', ax=axes[1])
axes[1].set_title('Price Comparison', fontsize=12)
axes[1].set_xlabel('Best Seller', fontsize=10)
axes[1].set_ylabel('Price (£)', fontsize=10)
axes[1].set_xticklabels(['Non-BestSeller', 'BestSeller'])

sns.boxplot(data=df, x='isBestSeller', y='boughtInLastMonth', ax=axes[2])
axes[2].set_title('Monthly Sales Comparison', fontsize=12)
axes[2].set_xlabel('Best Seller', fontsize=10)
axes[2].set_ylabel('Monthly Sales', fontsize=10)
axes[2].set_xticklabels(['Non-BestSeller', 'BestSeller'])

plt.tight_layout()
plt.savefig('output/visualization/bestseller_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print('\nBestSeller vs Non-BestSeller statistics:')
print('\n1. Star Rating:')
print(df.groupby('isBestSeller')['stars'].describe())
print('\n2. Price:')
print(df.groupby('isBestSeller')['price'].describe())
print('\n3. Monthly Sales:')
print(df.groupby('isBestSeller')['boughtInLastMonth'].describe())
print('BestSeller comparison chart generated')

# ==================== F. Sales by product tier ====================
print('\nF. Sales by Product Tier')
print('-' * 30)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

tier_order = ['Premium', 'Quality', 'Standard', 'Basic', 'Unknown']
tier_sales = df.groupby('product_tier')['boughtInLastMonth'].mean().reindex(tier_order)
sns.barplot(x=tier_sales.index, y=tier_sales.values, ax=ax1)
ax1.set_title('Average Monthly Sales by Product Tier', fontsize=14)
ax1.set_xlabel('Product Tier', fontsize=12)
ax1.set_ylabel('Average Monthly Sales', fontsize=12)
for i, v in enumerate(tier_sales.values):
    ax1.text(i, v, f'{v:.1f}', ha='center', va='bottom')

tier_counts = df['product_tier'].value_counts().reindex(tier_order)
sns.barplot(x=tier_counts.index, y=tier_counts.values, ax=ax2)
ax2.set_title('Product Count by Tier', fontsize=14)
ax2.set_xlabel('Product Tier', fontsize=12)
ax2.set_ylabel('Product Count', fontsize=12)
for i, v in enumerate(tier_counts.values):
    ax2.text(i, v, f'{v:,}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('output/visualization/product_tier_sales.png', dpi=300, bbox_inches='tight')
plt.close()

print('\nProduct tier sales statistics:')
print(df.groupby('product_tier')['boughtInLastMonth'].agg(['mean', 'median', 'count']).reindex(tier_order))
print('Product tier sales chart generated')

# ==================== G. Monthly sales by main category ====================
print('\nG. Monthly Sales Ranking by Main Category')
print('-' * 30)

category_sales = df.groupby('main_category')['boughtInLastMonth'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(15, 8))
sns.barplot(x=category_sales.values, y=category_sales.index, palette='viridis')
for i, v in enumerate(category_sales.values):
    plt.text(v, i, f' {v:,}', va='center')

plt.title('Top 10 Main Categories by Monthly Sales', fontsize=14)
plt.xlabel('Total Monthly Sales', fontsize=12)
plt.ylabel('Main Category', fontsize=12)
plt.tight_layout()
plt.savefig('output/visualization/category_sales_ranking.png', dpi=300, bbox_inches='tight')
plt.close()

print('\nTop 10 main category monthly sales stats:')
print(category_sales)
print('Main category monthly sales ranking chart generated')
