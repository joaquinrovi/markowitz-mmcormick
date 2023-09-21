# -*- coding: utf-8 -*-
"""
create_model.py
====================================
Functions for adding constraints and objectives to the optimization model.

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import *

def add_objective(model):
    """
    Add the objective function to the Markowitz portfolio optimization model.

    Parameters
    ----------
    model : ConcreteModel
        The Pyomo ConcreteModel representing the optimization problem.

    Returns
    -------
    None

    Notes
    -----
    This function defines the objective function, which is typically the maximization of expected return.

    Example
    -------
    To minimize risk, you can replace the objective with a risk-based objective.
    """
    # Objective: Maximize expected return

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
    model.obj_calculate_total_return = Objective(sense = maximize, rule = calculate_total_return)
    
    # Objective: Minimize risk
    
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
    # model.obj_calculate_total_risk = Objective(sense = minimize, rule = calculate_total_risk)


def add_constraints(model):
    """
    Add constraints to the Markowitz portfolio optimization model.

    Parameters
    ----------
    model : ConcreteModel
        The Pyomo ConcreteModel representing the optimization problem.

    Returns
    -------
    None

    Notes
    -----
    This function adds constraints to the optimization model, including the total weight constraint,
    the desired return constraint, and the linearized risk constraints.
    """
    def c_1_weights(model):
        '''
        Ensures the total weight sums up to one.

        Parameters
        ----------
        model : Pyomo ConcreteModel
            The optimization model.

        Returns
        -------
        Constraint Expression
        Relational expression for the constraint.
        '''
        weight_left = sum(model.w[i] for i in model.assets)
        weight_right = 1
        weight = (weight_left == weight_right)
        return weight
    model.c_1_weights = Constraint(rule=c_1_weights)

    def c_2_return(model):
        '''
        Ensures the desired level of return of the portfolio is accomplished

        Parameters
        ----------
        model : Pyomo ConcreteModel
            The optimization model.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        expected_return_left = sum(model.expected_return[i] * model.w[i] for i in model.assets)
        expected_return_right = model.return_level
        expected_return = (expected_return_left >= expected_return_right)
        return expected_return
    model.c_2_return = Constraint(rule=c_2_return)

    def c_3_1_linearized_risk(model):
        '''
        Linearizes the original MPT quadratic constraint by introducing an auxiliary variable.

        Parameters
        ----------

        model : Pyomo ConcreteModel
            The optimization model.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        auxiliary_1_left = sum(model.u[i,j] * model.covariance[i,j] for i in model.assets for j in model.assets)
        auxiliary_1_right = model.risk_level
        auxiliary_1 = (auxiliary_1_left <= auxiliary_1_right)
        return auxiliary_1
    model.c_3_1_linearized_risk = Constraint(rule = c_3_1_linearized_risk)

    def c_3_2_linearized_risk(model, i, j):
        '''
        Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

        Parameters
        ----------

        model : Pyomo ConcreteMode
            The optimization model.
        i : string
            The assets.
        j : string.
            The assets.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        lowBound = 0
        auxiliary_2_left = model.u[i,j]
        auxiliary_2_right = lowBound * model.w[j] + model.w[i] * lowBound  -  lowBound * lowBound
        auxiliary_2 = (auxiliary_2_left >= auxiliary_2_right)
        return auxiliary_2
    model.c_3_2_linearized_risk = Constraint(model.assets, model.assets, rule = c_3_2_linearized_risk)

    def c_3_3_linearized_risk(model, i, j):
        '''
        Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

        Parameters
        ----------

        model : Pyomo ConcreteMode
            The optimization model.
        i : string
            The assets.
        j : string.
            The assets.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        upperBound = 1
        auxiliary_3_left = model.u[i,j]
        auxiliary_3_right = upperBound * model.w[j] + model.w[i] * upperBound  -  upperBound * upperBound
        auxiliary_3 = (auxiliary_3_left >= auxiliary_3_right)
        return auxiliary_3
    model.c_3_3_linearized_risk = Constraint(model.assets, model.assets, rule = c_3_3_linearized_risk)

    def c_3_4_linearized_risk(model, i, j):
        '''
        Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

        Parameters
        ----------

        model : Pyomo ConcreteMode
            The optimization model.
        i : string
            The assets.
        j : string.
            The assets.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        lowBound = 0
        upperBound = 1
        auxiliary_4_left = model.u[i,j]
        auxiliary_4_right = upperBound * model.w[j] + model.w[i] * lowBound  -  upperBound * lowBound
        auxiliary_4 = (auxiliary_4_left <= auxiliary_4_right)
        return auxiliary_4
    model.c_3_4_linearized_risk = Constraint(model.assets, model.assets, rule = c_3_4_linearized_risk)

    def c_3_5_linearized_risk(model, i, j):
        '''
        Assigns bounds to the auxiliary variable for the linear convex relaxation (McCormick Envelopes).

        Parameters
        ----------

        model : Pyomo ConcreteMode
            The optimization model.
        i : string
            The assets.
        j : string.
            The assets.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        lowBound = 0
        upperBound = 1
        auxiliary_5_left = model.u[i,j]
        auxiliary_5_right = model.w[i] * upperBound  + lowBound * model.w[j]  -  lowBound * upperBound
        auxiliary_5 = (auxiliary_5_left <= auxiliary_5_right)
        return auxiliary_5
    model.c_3_5_linearized_risk = Constraint(model.assets, model.assets, rule = c_3_5_linearized_risk)

    def c_4_non_negative(model, i):
        '''
        Non negativity in the decision variable.

        Parameters
        ----------

        model : Pyomo ConcreteMode
            The optimization model.
        i : string
            The assets.
        j : string.
            The assets.

        Returns
        -------
        Constraint Expression
            Relational expression for the constraint.
        '''
        non_negative_left = model.w[i]
        non_negatiave_right = 0
        non_negative = (non_negative_left >= non_negatiave_right)
        return non_negative
    model.c_4_non_negative = Constraint(model.assets, rule = c_4_non_negative)
