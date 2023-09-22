# -*- coding: utf-8 -*-
"""
optimize.py
====================================
Run the optimizer (get the optimal portfolio)

@author:
     - j.rodriguez.villegas
"""

from pyomo.environ import SolverFactory, SolverStatus, TerminationCondition

from src.model.markowitz.preprocess_data import *
from src.model.markowitz.create_model import *
from src.model.markowitz.constraints import*
from src.model.markowitz.objective import *

if __name__ == "__main__":
    # Specify the path to the configuration file
    file_path = 'C:/Users/j.rodriguez.villegas/Documents/optimization/01_data/configuration_file.xlsx'
    sheet_name = 'Historical_data_2' # Change the sheet
    
    # Load data and create the optimization model
    df = read_data(file_path, sheet_name)
    assets_data = calculate_expected_return(df)
    pivot_table = create_pivot_table(df)
    covariance_matrix = calculate_covariance_matrix(pivot_table)
    model = create_optimization_model(assets_data, covariance_matrix)

    # Create constraints and objective
    create_contraints(model)
    create_objective(model)

    # Solve the linear convex problem
    solver = SolverFactory('glpk')
    solver.options['tmlim'] = 600
    result = solver.solve(model, tee=True, report_timing=True)

    # Check the solver's termination condition
    termination_condition = result.solver.termination_condition
    solver_status = result.solver.status

    # Print the results or handle them accordingly
    if solver_status == SolverStatus.ok and termination_condition == TerminationCondition.optimal:
        print("Optimal solution found.")
        total_return = calculate_total_return(model)
        print("Total Expected Return:", total_return)
        # Access and print the value of the objective function
        objective_value = value(model.obj_calculate_total_return)
        print("Objective Value:", objective_value)
    elif solver_status == SolverStatus.ok and termination_condition in [TerminationCondition.maxTimeLimit]:
        print("Time limit reached. No optimal solution found within the specified time.")
    else:
        print("No optimal solution found, model is infeasible or unbounded...")
        print("Solver terminated with condition:", solver_status)