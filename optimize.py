from src.model.markowitz.preprocess_data import *
from src.model.markowitz.create_model import *
from pyomo.environ import *

# Step 1: Preprocess data
file_path = 'C:/Users/j.rodriguez.villegas/Documents/optimization/01_data/configuration_file.xlsx'
sheet_name = 'Historical_data'
df = read_data(file_path, sheet_name)
pivot_table = pivot_data(df, "Date", "Asset", "ROI")
covariance_matrix = calculate_covariance_matrix(pivot_table)
correlation_matrix = calculate_correlation_matrix(pivot_table)
expected_return_data = calculate_expected_returns(df)

# Step 2: Create the optimization model
return_level = 0.001
risk_level = 0.0001
model = create_optimization_model(expected_return_data, return_level, risk_level, covariance_matrix)


solver = SolverFactory('glpk')

# Set the time limit in seconds
time_limit = 600  # 600 seconds
# Set the time limit in seconds
solver.options['tmlim'] = time_limit

# Solve the linear convex problem
result = solver.solve(model, tee=True, report_timing=True)

# Check the solver's termination condition
termination_condition = result.solver.termination_condition
solver_status = result.solver.status

# Print the results or handle them accordingly
if solver_status == SolverStatus.ok and termination_condition == TerminationCondition.optimal:
    optimal_solution = value(model.obj_calculate_total_return)
    print("Optimal solution found. Total expected return:", optimal_solution)
elif solver_status == SolverStatus.ok and termination_condition in [TerminationCondition.maxTimeLimit]:
    print("Time limit reached. No optimal solution found within the specified time.")
else:
    print("No optimal solution found, model is infeasible or unbounded...")
    print("Solver terminated with condition:", solver_status)