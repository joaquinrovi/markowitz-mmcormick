# -*- coding: utf-8 -*-
"""
preprocess_data.py
====================================
Functions to read, process and clean data.

@author:
     - j.rodriguez.villegas
"""
import pandas as pd
def main():
    
    # Basic data file reading
    file_path = 'your_file.xlsx'
    sheet_name = 'Sheet1'

    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Print the first 5 rows of the DataFrame
        print("First 5 rows of '{}' sheet:".format(sheet_name))
        print(df.head())

    except FileNotFoundError:
        print("File not found: '{}'".format(file_path))
    except Exception as e:
        print("An error occurred: {}".format(e))

if __name__ == '__main__':
    main()