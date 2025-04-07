#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure font to support Chinese labels if needed
plt.rcParams['font.sans-serif'] = ['SimHei']  # For displaying Chinese characters properly
plt.rcParams['axes.unicode_minus'] = False    # For displaying negative signs properly

print('=' * 50)
print('Starting Data Cleaning and Overview Analysis')
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

# ==================== 2. Drop Unnecessary Columns ====================
print('\n2. Dropping Unnecessary Columns')
print('-' * 30)
print(f'Columns before dropping: {df.columns.tolist()}')
df = df.drop(['imgUrl', 'productURL'], axis=1)
print(f'Columns after dropping: {df.columns.tolist()}')
print(f'Shape after cleaning: {df.shape}')

# ==================== 3. Price Distribution Overview ====================
print('\n3. Price Distribution Overview')
print('-' * 30)
price_stats = df['price'].describe()
print(f'Price Statistics:\n{price_stats}')

# Output outliers (price below 1 and above 1000)
low_price = df[df['price'] < 1]
high_price = df[df['price'] > 1000]
print(f'Number of products with price < 1: {len(low_price)}')
print(f'Number of products with price > 1000: {len(high_price)}')

# Check the 10 lowest and 10 highest prices
print(f'\nTop 10 Products with Lowest Prices:')
print(df.sort_values('price').head(10)[['asin', 'title', 'price', 'categoryName']])

print(f'\nTop 10 Products with Highest Prices:')
print(df.sort_values('price', ascending=False).head(10)[['asin', 'title', 'price', 'categoryName']])

# ==================== 4. Category Distribution Overview ====================
print('\n4. Category Distribution Overview')
print('-' * 30)
category_counts = df['categoryName'].value_counts()
print(f'Total number of categories: {len(category_counts)}')
print('\nTop 20 Categories and Product Counts:')
print(category_counts.head(20))

# ==================== 5. ASIN Duplication Overview ====================
print('\n5. ASIN Duplication Overview')
print('-' * 30)
duplicated_asin = df[df.duplicated('asin', keep=False)]
print(f'Total duplicated ASIN entries: {len(duplicated_asin)}')
print(f'Number of unique duplicated ASINs: {duplicated_asin["asin"].nunique()}')

if len(duplicated_asin) > 0:
    # Display top 5 most frequently duplicated ASINs
    dup_counts = duplicated_asin['asin'].value_counts().head(5)
    print('\nTop 5 Most Frequently Duplicated ASINs:')
    print(dup_counts)
    
    # Show all rows for the first duplicated ASIN
    first_dup_asin = dup_counts.index[0]
    print(f'\nDisplaying all records for first duplicated ASIN ({first_dup_asin}):')
    print(df[df['asin'] == first_dup_asin])

print('\nAnalysis Completed')
print('=' * 50)
