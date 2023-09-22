# -*- coding: utf-8 -*-
"""
objetive.py
====================================
Functions for the objectives of the mathematical model.

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import *

def create_objective(model):
    model.obj_calculate_total_return = Objective(sense=maximize, rule=calculate_total_return)
    # model.obj_calculate_total_risk = Objective(sense=minimize, rule=calculate_total_risk)


def calculate_total_return(model):
    '''
    This function calculates the total expected return on investment.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total expected return.
    '''
    total_return = sum(model.expected_return[i] * model.w[i] for i in model.assets)
    return total_return

def calculate_total_risk(model):
    '''
    This function calculates the total risk of the portfolio.

    Parameters
    ----------
    model : Pyomo ConcreteModel
        The optimization model.

    Return
    ------------
    double
        Total risk.
    '''
    total_risk = sum(model.u[i,j] * model.covariance[i,j] for i in model.assets for j in model.assets)
    return total_risk