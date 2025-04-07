#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

"""
Further Cleaning of Amazon Dataset and Feature Engineering
"""

# Create output directory
if not os.path.exists('output'):
    os.makedirs('output')

print('=' * 50)
print('Starting Further Data Cleaning and Feature Engineering')
print('=' * 50)

# ==================== 1. Load Cleaned CSV File ====================
print('\n1. Loading Cleaned CSV File')
print('-' * 30)

try:
    # Load from cleaned file if available; otherwise, load from raw and drop unnecessary columns
    if os.path.exists('output/amz_uk_cleaned_data.csv'):
        df = pd.read_csv('output/amz_uk_cleaned_data.csv')
        print('Successfully loaded cleaned file: output/amz_uk_cleaned_data.csv')
    else:
        df = pd.read_csv('archive/amz_uk_processed_data.csv')
        df = df.drop(['imgUrl', 'productURL'], axis=1)
        print('Loaded from raw file and dropped unnecessary columns')
    
    print(f'Data shape: {df.shape}')
except Exception as e:
    print(f'Error loading file: {e}')
    exit(1)

# ==================== 2. Handle Price Outliers ====================
print('\n2. Handling Price Outliers')
print('-' * 30)

# Show outlier stats
low_price = df[df['price'] < 1]
high_price = df[df['price'] > 1000]
print(f'Number of products with price = 0: {len(df[df["price"] == 0])}')
print(f'Number of products with price < 1: {len(low_price)}')
print(f'Number of products with price > 1000: {len(high_price)}')

# Filter out products with reasonable price range (1-1000 GBP)
df_filtered = df.copy()
df_filtered = df_filtered[(df_filtered['price'] >= 1) & (df_filtered['price'] <= 1000)]
print(f'Shape after filtering: {df_filtered.shape}')
print(f'Number of products filtered out: {df.shape[0] - df_filtered.shape[0]} '
      f'({(df.shape[0] - df_filtered.shape[0]) / df.shape[0] * 100:.2f}%)')

# ==================== 3. Feature Engineering ====================
print('\n3. Feature Engineering')
print('-' * 30)

# 1. Create price range feature
print('Creating price range feature...')
bins = [1, 10, 20, 50, 100, 200, 500, 1000]
labels = ['1-10', '10-20', '20-50', '50-100', '100-200', '200-500', '500-1000']
df_filtered['price_range'] = pd.cut(df_filtered['price'], bins=bins, labels=labels)

# Plot price range distribution
plt.figure(figsize=(12, 6))
df_filtered['price_range'].value_counts().sort_index().plot(kind='bar')
plt.title('Product Price Range Distribution')
plt.xlabel('Price Range (£)')
plt.ylabel('Number of Products')
plt.savefig('output/price_range_distribution.png')
plt.close()

# 2. Create main category feature (first word of category name)
print('Creating main category feature...')
df_filtered['main_category'] = df_filtered['categoryName'].apply(lambda x: x.split()[0] if isinstance(x, str) else 'Unknown')

# Plot main category distribution
plt.figure(figsize=(12, 8))
main_category_counts = df_filtered['main_category'].value_counts().head(15)
main_category_counts.plot(kind='barh')
plt.title('Top 15 Main Categories')
plt.xlabel('Number of Products')
plt.ylabel('Main Category')
plt.tight_layout()
plt.savefig('output/main_category_distribution.png')
plt.close()

# 3. Create product tier feature based on stars and review count
print('Creating product tier feature...')

def get_product_tier(row):
    stars = row['stars']
    reviews = row['reviews']
    
    if pd.isna(stars) or pd.isna(reviews):
        return 'Unknown'
    
    if stars >= 4.5 and reviews >= 1000:
        return 'Premium'
    elif stars >= 4.0 and reviews >= 100:
        return 'Quality'
    elif stars >= 3.5 and reviews >= 10:
        return 'Standard'
    else:
        return 'Basic'

df_filtered['product_tier'] = df_filtered.apply(get_product_tier, axis=1)

# Plot product tier distribution
plt.figure(figsize=(10, 6))
tier_order = ['Premium', 'Quality', 'Standard', 'Basic', 'Unknown']
tier_counts = df_filtered['product_tier'].value_counts().reindex(tier_order)
tier_counts.plot(kind='bar')
plt.title('Product Tier Distribution')
plt.xlabel('Product Tier')
plt.ylabel('Number of Products')
plt.savefig('output/product_tier_distribution.png')
plt.close()

# ==================== 4. Statistics and Visualization ====================
print('\n4. Statistics and Visualization')
print('-' * 30)

# 1. Average price by product tier
print('Analyzing average price per product tier...')
tier_price = df_filtered.groupby('product_tier')['price'].agg(['mean', 'median', 'count'])
print(tier_price)

plt.figure(figsize=(10, 6))
sns.barplot(x=df_filtered['product_tier'], y=df_filtered['price'], order=tier_order)
plt.title('Average Price by Product Tier')
plt.xlabel('Product Tier')
plt.ylabel('Average Price (£)')
plt.savefig('output/tier_avg_price.png')
plt.close()

# 2. Product tier distribution by top 10 main categories
print('Analyzing product tier distribution by top main categories...')
top10_categories = df_filtered['main_category'].value_counts().head(10).index
df_top_categories = df_filtered[df_filtered['main_category'].isin(top10_categories)]

plt.figure(figsize=(15, 10))
ax = sns.countplot(x='main_category', hue='product_tier', data=df_top_categories,
                  hue_order=tier_order, order=top10_categories)
plt.title('Product Tier Distribution by Top 10 Main Categories')
plt.xlabel('Main Category')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)
plt.legend(title='Product Tier')
plt.tight_layout()
plt.savefig('output/category_tier_distribution.png')
plt.close()

# ==================== 5. Save Further Cleaned Data ====================
print('\n5. Saving Further Cleaned Data')
print('-' * 30)

# Save cleaned and processed data
cleaned_file_path = 'output/amz_uk_further_cleaned.csv'
df_filtered.to_csv(cleaned_file_path, index=False)
print(f'Saved further cleaned data to: {cleaned_file_path}')

# Create summary report
with open('output/further_analysis_summary.txt', 'w', encoding='utf-8') as f:
    f.write('# Amazon UK Product Further Analysis Summary\n\n')
    f.write(f'## 1. Data Cleaning\n')
    f.write(f'- Original data shape: {df.shape[0]} rows x {df.shape[1]} columns\n')
    f.write(f'- Filtered data shape: {df_filtered.shape[0]} rows x {df_filtered.shape[1]} columns\n')
    f.write(f'- Number of products filtered out: {df.shape[0] - df_filtered.shape[0]} '
            f'({(df.shape[0] - df_filtered.shape[0])/df.shape[0]*100:.2f}%)\n\n')
    
    f.write(f'## 2. Price Analysis\n')
    f.write(f'- Filter condition: Price between 1 and 1000 GBP\n')
    f.write(f'- Price range distribution:\n')
    price_range_dist = df_filtered['price_range'].value_counts().sort_index()
    for range, count in price_range_dist.items():
        f.write(f'  * £{range}: {count} products ({count / df_filtered.shape[0] * 100:.2f}%)\n')
    
    f.write(f'\n## 3. Product Tier Analysis\n')
    f.write(f'- Product Tier Definitions:\n')
    f.write(f'  * Premium: Rating ≥ 4.5 and Reviews ≥ 1000\n')
    f.write(f'  * Quality: Rating ≥ 4.0 and Reviews ≥ 100\n')
    f.write(f'  * Standard: Rating ≥ 3.5 and Reviews ≥ 10\n')
    f.write(f'  * Basic: Others\n\n')
    
    f.write(f'- Product Tier Distribution:\n')
    tier_dist = df_filtered['product_tier'].value_counts().reindex(tier_order)
    for tier, count in tier_dist.items():
        f.write(f'  * {tier}: {count} products ({count / df_filtered.shape[0] * 100:.2f}%)\n')
    
    f.write(f'\n## 4. Average Price by Tier\n')
    for tier in tier_order:
        if tier in tier_price.index:
            f.write(f'- {tier}:\n')
            f.write(f'  * Number of Products: {tier_price.loc[tier, "count"]}\n')
            f.write(f'  * Average Price: £{tier_price.loc[tier, "mean"]:.2f}\n')
            f.write(f'  * Median Price: £{tier_price.loc[tier, "median"]:.2f}\n')

print('Saved further analysis summary to output/further_analysis_summary.txt')

print('\nFurther analysis and cleaning completed')
print('=' * 50)
