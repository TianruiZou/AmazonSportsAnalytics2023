#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Batch read all .csv files in the archive folder and merge them into a single DataFrame
"""

import pandas as pd
import os
import glob

def main():
    """
    Main function: read all CSV files and merge them
    """
    # File path pattern
    csv_path = 'archive/*.csv'
    
    # List to store all successfully read DataFrames
    all_dfs = []
    
    # Dictionary to store row count for each file
    file_stats = {}
    
    # Get all matching file paths
    csv_files = glob.glob(csv_path)
    
    if not csv_files:
        print(f"Warning: No .csv files found in the archive directory")
        return
    
    print(f"Found {len(csv_files)} CSV files...")
    
    # Iterate through each file and read
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        try:
            print(f"Reading file: {file_name}")
            
            # Try different encodings
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='latin1')
            
            # Add a column with the source file name
            df['source_file'] = file_name
            
            # Record row count
            file_stats[file_name] = len(df)
            
            # Append to list
            all_dfs.append(df)
            
            print(f"Successfully read {file_name} with {len(df)} rows")
        
        except Exception as e:
            print(f"Failed to read file {file_name}: {str(e)}")
    
    # Check if any files were read successfully
    if not all_dfs:
        print("Error: No files were successfully read")
        return
    
    # Merge all DataFrames
    try:
        df_all = pd.concat(all_dfs, ignore_index=True)
        print("\nFiles merged successfully!")
        
        # Print merged data info
        print(f"\nMerged data dimensions (rows, columns): {df_all.shape}")
        
        print("\nColumn names:")
        print(df_all.columns.tolist())
        
        # Show number of rows contributed by each file
        print("\nNumber of rows from each file:")
        file_counts = df_all.groupby('source_file').size()
        for file_name, count in file_counts.items():
            print(f"{file_name}: {count} rows")
        
        print("\nPreview of first 5 rows:")
        print(df_all.head())
        
        # Optionally: save the merged data
        df_all.to_csv('merged_data.csv', index=False)
        print("\nMerged data saved to merged_data.csv")
        
    except Exception as e:
        print(f"Error merging files: {str(e)}")

if __name__ == "__main__":
    main()
