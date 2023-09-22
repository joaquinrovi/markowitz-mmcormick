# -*- coding: utf-8 -*-
"""
create_model.py
====================================
Function for the mathematical model (Sets, Parameters and Variables).

@author:
     - j.rodriguez.villegas
"""
from pyomo.environ import *

def create_optimization_model(assets_data, covariance_matrix):
    '''
    Create a Markowitz portfolio optimization model.

    Parameters
    ----------
    assets_data : DataFrame
        A DataFrame containing asset data, including expected returns.
    covariance_matrix : DataFrame
        A DataFrame containing the covariance matrix of asset returns.

    Returns
    -------
    ConcreteModel
        The created Pyomo ConcreteModel for portfolio optimization.
    '''
    model = ConcreteModel('markowitz')
    
    # Extract assets from the columns of the covariance_matrix DataFrame
    assets = list(covariance_matrix.columns)
    
    model.assets = Set(initialize=assets)  # Use the assets extracted from covariance_matrix
    
    model.return_level = Param(initialize=0.001)
    model.risk_level = Param(initialize=0.001)
    model.expected_return = Param(model.assets, initialize=assets_data.set_index('Asset')["Mean (average) ROI"].to_dict())

    # Define and initialize covariance parameter
    covariance_dict = {(i, j): covariance_matrix.at[i, j] for i in assets for j in assets}
    model.covariance = Param(model.assets, model.assets, initialize=covariance_dict)

    model.w = Var(model.assets, domain=NonNegativeReals, bounds=(0, 1))
    model.u = Var(model.assets, model.assets, domain=NonNegativeReals)
    
    return model