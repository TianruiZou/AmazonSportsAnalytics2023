#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

# Read the data
df = pd.read_csv('output/amz_uk_further_cleaned.csv')

# Print main category statistics
print('Main Category Statistics:')
print(df['main_category'].value_counts())

# Print all unique main category names
print('\nAll Unique Main Categories:')
for category in sorted(df['main_category'].unique()):
    print(f'- {category}')
