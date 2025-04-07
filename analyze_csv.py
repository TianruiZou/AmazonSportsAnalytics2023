#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# File path
file_path = 'archive/amz_uk_processed_data.csv'

print('=' * 50)
print('Starting CSV file analysis')
print('=' * 50)

# ==================== 1. Read CSV File ====================
print('\n1. Reading CSV File')
print('-' * 30)
try:
    # Try to read the file
    df = pd.read_csv(file_path)
    print(f'Successfully read file: {file_path}')
except Exception as e:
    print(f'Error reading file: {e}')
    exit(1)

# ==================== 2. Display Data Dimensions ====================
print('\n2. Data Dimensions (Rows and Columns)')
print('-' * 30)
print(f'Number of rows: {df.shape[0]}')
print(f'Number of columns: {df.shape[1]}')

# ==================== 3. Display Column Names ====================
print('\n3. Column Names')
print('-' * 30)
for i, col in enumerate(df.columns):
    print(f'{i+1}. {col}')

# ==================== 4. Display First Five Rows ====================
print('\n4. First Five Rows of Data')
print('-' * 30)
print(df.head(5))

# ==================== 5. Missing Value Statistics ====================
print('\n5. Missing Value Statistics')
print('-' * 30)
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Values': missing_values,
    'Missing Percentage (%)': missing_percent.round(2)
})
print(missing_df)

# ==================== 6. Data Types of Each Column ====================
print('\n6. Data Types')
print('-' * 30)
dtypes_df = pd.DataFrame({
    'Data Type': df.dtypes
})
print(dtypes_df)

print('\nAnalysis Completed')
print('=' * 50)
