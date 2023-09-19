# -*- coding: utf-8 -*-
"""
create_model.py
====================================
Framework of the mathematical model.

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import *
from src.model.markowitz.constraints import add_constraints, add_objective


def create_optimization_model(assets_data, return_level, risk_level, covariance_matrix):
    """
    Creates the Markowitz-McCormick portfolio optimization problem.

    Parameters
    ----------
    assets_data : DataFrame
        DataFrame containing asset data, including the Mean (average) ROI.
    return_level : float
        The desired level of portfolio return.
    risk_level : float
        The desired level of portfolio risk.
    covariance_matrix : DataFrame
        DataFrame containing the covariance matrix of asset returns.

    Returns
    -------
    ConcreteModel
        The Pyomo ConcreteModel representing the optimization problem.

    Notes
    -----
    This function sets up the mathematical framework for the Markowitz portfolio optimization problem. It defines
    sets, parameters, decision variables, and placeholders for constraints and objectives to be added later.

    Example
    -------
    model = create_optimization_model(assets_data, 0.001, 0.0001, covariance_matrix)
    # Further define constraints and objectives, then solve the optimization problem.
    """
    model = ConcreteModel('markowitz')

    # Sets
    model.assets = Set(initialize=assets_data.index)

    # Parameters
    model.return_level = Param(initialize=return_level)
    model.risk_level = Param(initialize=risk_level)
    model.expected_return = Param(model.assets, initialize=assets_data['Mean (average) ROI'].to_dict())
    model.covariance = Param(model.assets, model.assets, initialize=covariance_matrix.values.tolist(), mutable=True)

    # Decision variables
    model.w = Var(model.assets, domain=NonNegativeReals, bounds=(0, 1))
    model.u = Var(model.assets, model.assets, domain=NonNegativeReals)

    # Add constraints
    add_constraints(model)

    # Add objective function
    add_objective(model)

    return model

