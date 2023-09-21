# -*- coding: utf-8 -*-
"""
preprocess_data.py
====================================
Functions to read, process and clean data.

@author:
     - j.rodriguez.villegas
"""
import pandas as pd

def read_data(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name = sheet_name)
    return df

def create_pivot_table(df):
    pivot_table = df.pivot(index="Date", columns="Asset", values="ROI")
    return pivot_table

def calculate_covariance_matrix(pivot_table):
    covariance_matrix = pivot_table.cov()
    return covariance_matrix

def calculate_expected_return(df):
    assets_df = df.groupby("Asset")["ROI"].mean().reset_index()
    assets_df.rename(columns={"ROI": "Mean (average) ROI"}, inplace=True)
    return assets_df