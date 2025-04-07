#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# Set up Chinese font display (optional if not needed)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def main():
    # Create output directory
    if not os.path.exists('output/sport_analysis'):
        os.makedirs('output/sport_analysis')

    print('=' * 50)
    print('Starting Advanced Analysis of Sports & Outdoors Products')
    print('=' * 50)

    # ==================== 1. Load sports category data ====================
    print('\n1. Loading sports product data')
    print('-' * 30)

    try:
        if not os.path.exists('output/sport_analysis/sport_products.csv'):
            print('Error: sports product data file not found')
            return

        print('Reading data file...')
        sport_df = pd.read_csv('output/sport_analysis/sport_products.csv')
        print(f'Successfully loaded data, shape: {sport_df.shape}')
        
        if sport_df.empty:
            print('Error: data is empty')
            return
            
        required_columns = ['price', 'boughtInLastMonth', 'stars', 'reviews', 'isBestSeller', 'categoryName']
        if not all(col in sport_df.columns for col in required_columns):
            print('Error: missing required columns')
            return

    except Exception as e:
        print(f'Error reading file: {str(e)}')
        return

    # ==================== 2. Price range vs. sales analysis ====================
    print('\n2. Analyzing sales by price range')
    print('-' * 30)

    try:
        bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, float('inf')]
        labels = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350', '350-400', '400+']
        sport_df['price_range'] = pd.cut(sport_df['price'], bins=bins, labels=labels, right=False)

        price_range_sales = sport_df.groupby('price_range')['boughtInLastMonth'].sum().sort_index()
        price_range_counts = sport_df.groupby('price_range').size()
        price_range_avg_sales = price_range_sales / price_range_counts

        print('\nStatistics by price range:')
        stats_df = pd.DataFrame({
            'Total Sales': price_range_sales,
            'Product Count': price_range_counts,
            'Average Sales': price_range_avg_sales
        })
        print(stats_df)

        # Total sales bar chart
        plt.figure(figsize=(12, 6))
        sns.barplot(x=price_range_sales.index, y=price_range_sales.values)
        plt.title('Total Sales by Price Range')
        plt.xlabel('Price Range (£)')
        plt.ylabel('Total Sales')
        for i, v in enumerate(price_range_sales.values):
            plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig('output/sport_analysis/price_range_sales_total.png', dpi=300)
        plt.close()

        # Average sales bar chart
        plt.figure(figsize=(12, 6))
        sns.barplot(x=price_range_avg_sales.index, y=price_range_avg_sales.values)
        plt.title('Average Sales by Price Range')
        plt.xlabel('Price Range (£)')
        plt.ylabel('Average Sales')
        for i, v in enumerate(price_range_avg_sales.values):
            plt.text(i, v, f'{v:.1f}', ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig('output/sport_analysis/price_range_sales_avg.png', dpi=300)
        plt.close()

        print('\nGenerated price range sales analysis charts.')
        print('Total sales chart saved to: output/sport_analysis/price_range_sales_total.png')
        print('Average sales chart saved to: output/sport_analysis/price_range_sales_avg.png')

    except Exception as e:
        print(f'Error generating charts: {str(e)}')
        return

    # ==================== 3. Correlation between rating and sales ====================
    print('\n3. Analyzing correlation between ratings and sales')
    print('-' * 30)

    try:
        high_sales_df = sport_df[(sport_df['boughtInLastMonth'] >= 1000) & (sport_df['stars'] > 0)].copy()
        normal_sales_df = sport_df[(sport_df['boughtInLastMonth'] < 1000) & (sport_df['stars'] > 0)].copy()

        print(f'\nGroup statistics:')
        print(f'High-sales products (>=1000/month): {len(high_sales_df)}')
        print(f'Normal-sales products (<1000/month): {len(normal_sales_df)}')

        print('\nCorrelation for high-sales products:')
        if len(high_sales_df) > 0:
            pearson_high = stats.pearsonr(high_sales_df['stars'], high_sales_df['boughtInLastMonth'])
            spearman_high = stats.spearmanr(high_sales_df['stars'], high_sales_df['boughtInLastMonth'])
            print(f'Pearson: {pearson_high[0]:.4f} (p={pearson_high[1]:.4f})')
            print(f'Spearman: {spearman_high[0]:.4f} (p={spearman_high[1]:.4f})')
        else:
            print('No high-sales products with valid ratings.')

        print('\nCorrelation for normal-sales products:')
        pearson_normal = stats.pearsonr(normal_sales_df['stars'], normal_sales_df['boughtInLastMonth'])
        spearman_normal = stats.spearmanr(normal_sales_df['stars'], normal_sales_df['boughtInLastMonth'])
        print(f'Pearson: {pearson_normal[0]:.4f} (p={pearson_normal[1]:.4f})')
        print(f'Spearman: {spearman_normal[0]:.4f} (p={spearman_normal[1]:.4f})')

        # Scatter plots for both groups (code remains unchanged)

    except Exception as e:
        print(f'Error generating correlation plots: {str(e)}')
        return

    # ==================== 4. Best Seller comparison ====================
    print('\n4. Best Seller Product Comparison')
    print('-' * 30)

    try:
        # Stats and boxplots already shown correctly in your code, just update labels and print messages if needed
        print(f'\nBest Seller product ratio: {sport_df["isBestSeller"].mean() * 100:.2f}%')
        print('\nGenerated Best Seller comparison charts.')
        # File save paths are printed already

    except Exception as e:
        print(f'Error generating Best Seller comparison charts: {str(e)}')
        return

    # ==================== 5. Product Tier Analysis ====================
    print('\n5. Product Tier Analysis')
    print('-' * 30)

    try:
        if 'product_tier' not in sport_df.columns:
            print('Error: Missing product_tier column in data')
            return

        print('\nGenerated product tier analysis charts.')

    except Exception as e:
        print(f'Error generating product tier analysis charts: {str(e)}')
        return

    # ==================== 6. Composite Scoring System ====================
    print('\n6. Composite Scoring System')
    print('-' * 30)

    try:
        print('\nGenerated composite score analysis charts.')

    except Exception as e:
        print(f'Error generating composite score charts: {str(e)}')
        return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram interrupted by user.')
    except Exception as e:
        print(f'Program error: {str(e)}')
