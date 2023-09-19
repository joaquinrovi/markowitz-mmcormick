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
    """
    Reads data from an Excel file and returns it as a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        The file path to the Excel file.
    sheet_name : str
        The name of the Excel sheet to read.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the data from the specified sheet.

    Raises
    ------
    FileNotFoundError
        If the specified file cannot be found.
    pd.errors.ParserError
        If there is an issue parsing the Excel file.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.ParserError:
        raise pd.errors.ParserError(f"Error parsing the Excel file: {file_path}")

def pivot_data(df, index_col, columns_col, values_col):
    """
    Pivots a DataFrame to create a pivot table.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing data.
    index_col : str
        The column to be used as the index in the pivot table.
    columns_col : str
        The column to be used as the columns in the pivot table.
    values_col : str
        The column to be used as the values in the pivot table.

    Returns
    -------
    pd.DataFrame
        A pivot table containing the specified index, columns, and values.
    """
    pivot_table = df.pivot(index=index_col, columns=columns_col, values=values_col)
    return pivot_table

def calculate_covariance_matrix(pivot_table):
    """
    Calculates the covariance matrix from a pivot table of asset returns.

    Parameters
    ----------
    pivot_table : pd.DataFrame
        The pivot table containing asset returns.

    Returns
    -------
    pd.DataFrame
        A covariance matrix of asset returns.
    """
    covariance_matrix = pivot_table.cov()
    return covariance_matrix

def calculate_correlation_matrix(pivot_table):
    """
    Calculates the correlation matrix from a pivot table of asset returns.

    Parameters
    ----------
    pivot_table : pd.DataFrame
        The pivot table containing asset returns.

    Returns
    -------
    pd.DataFrame
        A correlation matrix of asset returns.
    """
    correlation_matrix = pivot_table.corr()
    return correlation_matrix

def calculate_expected_returns(df):
    """
    Calculates the expected returns of assets from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing asset data.

    Returns
    -------
    pd.DataFrame
        A DataFrame with asset names and their corresponding mean (average) ROI.
    """
    assets_df = df.groupby("Asset")["ROI"].mean().reset_index()
    assets_df.rename(columns={"ROI": "Mean (average) ROI"}, inplace=True)
    return assets_df
