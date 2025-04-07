#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directory
if not os.path.exists('output'):
    os.makedirs('output')

# Configure font to support Chinese labels if needed
plt.rcParams['font.sans-serif'] = ['SimHei']  # For displaying Chinese characters correctly
plt.rcParams['axes.unicode_minus'] = False    # For displaying negative signs correctly

print('=' * 50)
print('Starting data cleaning and saving')
print('=' * 50)

# ==================== 1. Read CSV File ====================
print('\n1. Reading CSV File')
print('-' * 30)
file_path = 'archive/amz_uk_processed_data.csv'
try:
    df = pd.read_csv(file_path)
    print(f'Successfully read file: {file_path}')
    print(f'Original data shape: {df.shape}')
except Exception as e:
    print(f'Error reading file: {e}')
    exit(1)

# ==================== 2. Drop Unnecessary Columns and Save ====================
print('\n2. Dropping Unnecessary Columns')
print('-' * 30)
print(f'Columns before dropping: {df.columns.tolist()}')
df_cleaned = df.drop(['imgUrl', 'productURL'], axis=1)
print(f'Columns after dropping: {df_cleaned.columns.tolist()}')
print(f'Data shape after cleaning: {df_cleaned.shape}')

# Save cleaned data
cleaned_file_path = 'output/amz_uk_cleaned_data.csv'
df_cleaned.to_csv(cleaned_file_path, index=False)
print(f'Saved cleaned data to: {cleaned_file_path}')

# ==================== 3. Price Analysis and Visualization ====================
print('\n3. Price Distribution Analysis')
print('-' * 30)
price_stats = df_cleaned['price'].describe()
print(f'Price Statistics:\n{price_stats}')

# Count extreme values
low_price = df_cleaned[df_cleaned['price'] < 1]
high_price = df_cleaned[df_cleaned['price'] > 1000]
print(f'Number of products with price < 1: {len(low_price)}')
print(f'Number of products with price > 1000: {len(high_price)}')

# Plot histogram of prices (excluding outliers)
plt.figure(figsize=(12, 6))
sns.histplot(df_cleaned[(df_cleaned['price'] > 0) & (df_cleaned['price'] <= 1000)]['price'], bins=50)
plt.title('Product Price Distribution Histogram (£0-1000)')
plt.xlabel('Price (£)')
plt.ylabel('Number of Products')
plt.savefig('output/price_distribution.png')
plt.close()

# Plot boxplot of prices (excluding extreme values)
plt.figure(figsize=(10, 6))
sns.boxplot(x=df_cleaned[(df_cleaned['price'] > 0) & (df_cleaned['price'] <= 500)]['price'])
plt.title('Product Price Boxplot (£0-500)')
plt.xlabel('Price (£)')
plt.savefig('output/price_boxplot.png')
plt.close()

# ==================== 4. Category Analysis and Visualization ====================
print('\n4. Category Distribution Analysis')
print('-' * 30)
category_counts = df_cleaned['categoryName'].value_counts()
print(f'Total number of categories: {len(category_counts)}')
print('\nTop 20 categories and product counts:')
print(category_counts.head(20))

# Bar chart for top 20 categories
plt.figure(figsize=(15, 10))
category_counts.head(20).plot(kind='barh')
plt.title('Top 20 Product Categories')
plt.xlabel('Number of Products')
plt.ylabel('Category Name')
plt.tight_layout()
plt.savefig('output/top20_categories.png')
plt.close()

# Pie chart for top 20 categories + others
plt.figure(figsize=(12, 12))
others = category_counts.iloc[20:].sum()
pie_data = pd.concat([category_counts.head(20), pd.Series([others], index=['Other Categories'])])
plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Category Proportion (Top 20 + Others)')
plt.tight_layout()
plt.savefig('output/category_pie_chart.png')
plt.close()

# ==================== 5. ASIN Duplication Check ====================
print('\n5. ASIN Duplication Check')
print('-' * 30)
duplicated_asin = df_cleaned[df_cleaned.duplicated('asin', keep=False)]
print(f'Number of duplicated ASIN entries: {len(duplicated_asin)}')
print(f'Number of unique duplicated ASINs: {duplicated_asin["asin"].nunique()}')

# ==================== 6. Save Summary of Analysis ====================
print('\n6. Saving Summary of Analysis')
print('-' * 30)

# Create summary file
with open('output/data_analysis_summary.txt', 'w', encoding='utf-8') as f:
    f.write('# Amazon UK Product Data Analysis Summary\n\n')
    f.write(f'## 1. Data Overview\n')
    f.write(f'- Total number of products: {df_cleaned.shape[0]}\n')
    f.write(f'- Total number of categories: {len(category_counts)}\n\n')
    
    f.write(f'## 2. Price Analysis\n')
    f.write(f'- Average price: £{price_stats["mean"]:.2f}\n')
    f.write(f'- Median price: £{price_stats["50%"]:.2f}\n')
    f.write(f'- Minimum price: £{price_stats["min"]:.2f}\n')
    f.write(f'- Maximum price: £{price_stats["max"]:.2f}\n')
    f.write(f'- Number of products with price < 1: {len(low_price)}\n')
    f.write(f'- Number of products with price > 1000: {len(high_price)}\n\n')
    
    f.write(f'## 3. Top Categories\n')
    for i, (cat, count) in enumerate(category_counts.head(10).items()):
        f.write(f'{i+1}. {cat}: {count} items\n')

print('Saved summary to output/data_analysis_summary.txt')

print('\nData cleaning and analysis completed')
print('=' * 50)
