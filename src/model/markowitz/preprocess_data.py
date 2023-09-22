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
    '''
    Reads data from an Excel file into a DataFrame.

    Parameters
    ----------
    file_path : str
        The path to the Excel file.
    sheet_name : str
        The name of the sheet within the Excel file to read.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the data from the specified Excel sheet.
    '''
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

def create_pivot_table(df):
    '''
    Creates a pivot table from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A pivot table with "Date" as the index, "Asset" as columns, and "ROI" as values.
    '''
    pivot_table = df.pivot(index="Date", columns="Asset", values="ROI")
    return pivot_table

def calculate_covariance_matrix(pivot_table):
    '''
    Calculates the covariance matrix from a pivot table.

    Parameters
    ----------
    pivot_table : pd.DataFrame
        The pivot table containing asset returns.

    Returns
    -------
    pd.DataFrame
        The covariance matrix of asset returns.
    '''
    covariance_matrix = pivot_table.cov()
    return covariance_matrix

def calculate_expected_return(df):
    '''
    Calculates the expected return for each asset.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with asset names and their corresponding mean (average) ROI.
    '''
    assets_df = df.groupby("Asset")["ROI"].mean().reset_index()
    assets_df.rename(columns={"ROI": "Mean (average) ROI"}, inplace=True)
    return assets_df