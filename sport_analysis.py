#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Set font to display Chinese labels if needed
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def main():
    # Create output directory
    if not os.path.exists('output/sport_analysis'):
        os.makedirs('output/sport_analysis')

    print('=' * 50)
    print('Starting Sports & Outdoors Product Analysis')
    print('=' * 50)

    # ==================== 1. Read cleaned data ====================
    print('\n1. Reading cleaned data')
    print('-' * 30)

    try:
        if not os.path.exists('output/amz_uk_further_cleaned.csv'):
            print('Error: data file not found')
            return

        print('Reading data file...')
        df = pd.read_csv('output/amz_uk_further_cleaned.csv')
        print(f'Data loaded successfully, shape: {df.shape}')
        
        if df.empty:
            print('Error: data is empty')
            return

        if 'main_category' not in df.columns:
            print('Error: main_category column missing in data')
            return
            
        print(f'Columns: {df.columns.tolist()}')
        print(f'Unique main categories: {df["main_category"].unique()}')

    except Exception as e:
        print(f'Error reading file: {str(e)}')
        return

    # ==================== 2. Filter Sports products ====================
    print('\n2. Filtering Sports & Outdoors products')
    print('-' * 30)

    try:
        sport_df = df[df['main_category'] == 'Sports'].copy()
        print(f'Number of Sports products: {len(sport_df)}')

        if len(sport_df) == 0:
            print('Warning: No Sports products found')
            return

        sport_df.to_csv('output/sport_analysis/sport_products.csv', index=False)
        print('Saved Sports products to output/sport_analysis/sport_products.csv')

    except Exception as e:
        print(f'Error processing data: {str(e)}')
        return

    # ==================== 3. Visualization ====================
    print('\n3. Starting Visualization')
    print('-' * 30)

    try:
        # a. Price distribution
        print('\na. Price distribution analysis')
        plt.figure(figsize=(12, 6))
        price_filtered = sport_df[sport_df['price'] < 500]
        sns.histplot(data=price_filtered, x='price', bins=50)
        plt.title('Price Distribution of Sports Products (Price < 500)', fontsize=14)
        plt.xlabel('Price (£)', fontsize=12)
        plt.ylabel('Number of Products', fontsize=12)
        plt.tight_layout()
        plt.savefig('output/sport_analysis/price_distribution.png', dpi=300)
        plt.close()
        print('Price distribution chart generated')

        # b. Star rating distribution
        print('\nb. Star rating distribution analysis')
        plt.figure(figsize=(12, 6))
        sns.countplot(data=sport_df, x='stars')
        plt.title('Star Rating Distribution of Sports Products', fontsize=14)
        plt.xlabel('Star Rating', fontsize=12)
        plt.ylabel('Number of Products', fontsize=12)
        plt.tight_layout()
        plt.savefig('output/sport_analysis/stars_distribution.png', dpi=300)
        plt.close()
        print('Star rating chart generated')

        # c. Review count distribution
        print('\nc. Review count distribution analysis')
        plt.figure(figsize=(12, 6))
        reviews_filtered = sport_df[sport_df['reviews'] < 2000]
        sns.histplot(data=reviews_filtered, x='reviews', bins=50)
        plt.title('Review Count Distribution (Reviews < 2000)', fontsize=14)
        plt.xlabel('Number of Reviews', fontsize=12)
        plt.ylabel('Number of Products', fontsize=12)
        plt.tight_layout()
        plt.savefig('output/sport_analysis/reviews_distribution.png', dpi=300)
        plt.close()
        print('Review count chart generated')

        # d. Sales vs. Rating
        print('\nd. Monthly Sales vs. Star Rating')
        plt.figure(figsize=(12, 6))
        sales_filtered = sport_df[sport_df['boughtInLastMonth'] < 1000]
        sns.scatterplot(data=sales_filtered, x='stars', y='boughtInLastMonth', alpha=0.5)
        plt.title('Monthly Sales vs. Star Rating (Sales < 1000)', fontsize=14)
        plt.xlabel('Star Rating', fontsize=12)
        plt.ylabel('Monthly Sales', fontsize=12)
        plt.tight_layout()
        plt.savefig('output/sport_analysis/sales_stars_relation.png', dpi=300)
        plt.close()
        print('Monthly Sales vs. Rating chart generated')

        # e. BestSeller vs Non-BestSeller Comparison
        print('\ne. BestSeller vs Non-BestSeller Comparison')
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        sns.boxplot(data=sport_df, x='isBestSeller', y='stars', ax=axes[0])
        axes[0].set_title('Star Rating Comparison')
        axes[0].set_xlabel('Best Seller')
        axes[0].set_ylabel('Star Rating')
        axes[0].set_xticklabels(['Not Best Seller', 'Best Seller'])

        sns.boxplot(data=sport_df[sport_df['price'] < 500], x='isBestSeller', y='price', ax=axes[1])
        axes[1].set_title('Price Comparison (Price < 500)')
        axes[1].set_xlabel('Best Seller')
        axes[1].set_ylabel('Price (£)')
        axes[1].set_xticklabels(['Not Best Seller', 'Best Seller'])

        sns.boxplot(data=sport_df[sport_df['boughtInLastMonth'] < 1000], x='isBestSeller', y='boughtInLastMonth', ax=axes[2])
        axes[2].set_title('Sales Comparison (Monthly Sales < 1000)')
        axes[2].set_xlabel('Best Seller')
        axes[2].set_ylabel('Monthly Sales')
        axes[2].set_xticklabels(['Not Best Seller', 'Best Seller'])

        plt.tight_layout()
        plt.savefig('output/sport_analysis/bestseller_comparison.png', dpi=300)
        plt.close()
        print('BestSeller comparison chart generated')

        # f. Product tier sales difference
        print('\nf. Product Tier Sales Difference')
        plt.figure(figsize=(12, 6))
        tier_sales = sport_df.groupby('product_tier')['boughtInLastMonth'].mean().sort_values(ascending=False)
        sns.barplot(x=tier_sales.index, y=tier_sales.values)
        plt.title('Average Sales by Product Tier (Sports)', fontsize=14)
        plt.xlabel('Product Tier', fontsize=12)
        plt.ylabel('Average Monthly Sales', fontsize=12)
        plt.tight_layout()
        plt.savefig('output/sport_analysis/tier_sales_comparison.png', dpi=300)
        plt.close()
        print('Product tier sales comparison chart generated')

        # g. Sales by price range
        print('\ng. Sales by Price Range')
        bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, float('inf')]
        labels = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400+']
        sport_df['price_range'] = pd.cut(sport_df['price'], bins=bins, labels=labels, right=False)
        price_range_sales = sport_df.groupby('price_range')['boughtInLastMonth'].sum().sort_index()

        plt.figure(figsize=(12, 6))
        sns.barplot(x=price_range_sales.index, y=price_range_sales.values)
        plt.title('Total Sales by Price Range (Sports)', fontsize=14)
        plt.xlabel('Price Range (£)', fontsize=12)
        plt.ylabel('Total Sales', fontsize=12)
        for i, v in enumerate(price_range_sales.values):
            plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig('output/sport_analysis/price_range_sales.png', dpi=300)
        plt.close()

        print('\nSales by Price Range Statistics:')
        print(price_range_sales)
        print('Price range sales chart generated')

    except Exception as e:
        print(f'Error generating charts: {str(e)}')
        return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram interrupted by user')
    except Exception as e:
        print(f'Program execution error: {str(e)}')
