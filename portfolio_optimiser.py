from matrix_library import *
from matplotlib import pyplot as plt
import math

# expected returns
expected_returns = [0.10, 0.08, 0.12] 

# covariance matrix
cov_mat = [
    [0.04, 0.01, 0.02],
    [0.01, 0.09, 0.03],
    [0.02, 0.03, 0.16]
]

# finds the portfolio expected return based on weights and expected returns of each asset
def portfolio_return(weights, expected_returns):
    return dot_product(weights, expected_returns)

# portfolio variance calculator
def portfolio_variance(weights, covariance_matrix):
    weights_rows, _ = matrix_shape(vector_to_column_matrix(weights))
    _, cov_mat_columns = matrix_shape(covariance_matrix)

    # portfolio variance can only be calculated if dimensions are compatible
    if weights_rows != cov_mat_columns:
        print("Error! weights and covariance matrix must have appropriate dimensions")
        return None
    else:
        vct = transpose(vector_to_column_matrix(weights))
        a = matrix_multiplication(vct, covariance_matrix)
        result = matrix_multiplication(a, vector_to_column_matrix(weights))
        return result[0][0]

# finds the optimal weights for each asset
def optimal_weights(covariance_matrix):
    # convert vectors into matrix form 
    rows, columns = matrix_shape(covariance_matrix)
    vct_1 = []
    for _ in range(rows):
        vct_1.append(1)
    vector_of_ones = vector_to_column_matrix(vct_1)

    # obtain inverse of covariance matrix
    inv_cov_mat = inverse(covariance_matrix)

    # solve for lambda
    x = matrix_multiplication(transpose(vector_of_ones), matrix_multiplication(inv_cov_mat, vector_of_ones))

    # convert 1x1 matrix to float
    x = x[0][0]

    lam = 2/x

    # obtain weights by substituting lambda into minimisation expression to get optimal weights
    weights = matrix_scalar_multiplication(matrix_multiplication(inv_cov_mat, vector_of_ones), lam/2)
    return column_matrix_to_vector(weights)

# finds the optimal weights for each asset given a target return
def optimal_weights_for_return(expected_returns, covariance_matrix, target_return):
    # convert vectors into matrix form
    rows, _ = matrix_shape(covariance_matrix)
    vct_1 = []
    for _ in range(rows):
        vct_1.append(1)
    vector_of_ones = vector_to_column_matrix(vct_1)

    exp_returns = vector_to_column_matrix(expected_returns)

    # obtain inverse of covariance matrix
    inv_cov_mat = inverse(covariance_matrix)

    # obtain coefficients for system of equations 
    a = matrix_multiplication(matrix_multiplication(transpose(vector_of_ones), inv_cov_mat), vector_of_ones)
    b = matrix_multiplication(matrix_multiplication(transpose(vector_of_ones), inv_cov_mat), exp_returns)
    c = matrix_multiplication(matrix_multiplication(transpose(exp_returns), inv_cov_mat), exp_returns)

    # make 1x1 matrix into float
    a = a[0][0]
    b = b[0][0]
    c = c[0][0]

    # solve system of equations
    coefficient_matrix = [[a, b], [b, c]]
    constant_vct= [2, 2 * target_return]
    lam1, lam2 = system_solver(coefficient_matrix, constant_vct)

    # obtain weights vector w
    term1 = matrix_scalar_multiplication(matrix_multiplication(inv_cov_mat, vector_of_ones), lam1/2)
    term2 = matrix_scalar_multiplication(matrix_multiplication(inv_cov_mat, exp_returns), lam2/2)
    w = matrix_addition(term1, term2)

    # convert into vector represenation
    return column_matrix_to_vector(w)

# finds the optimal weights for each asset while maxmimising the sharpe ratio
def optimal_weights_sharpe(expected_returns, covariance_matrix, risk_free_rate):

    # convert vectors to matrix form
    expected_returns = vector_to_column_matrix(expected_returns)
    rows, _ = matrix_shape(expected_returns)

    # form the vector of ones
    vector_of_ones = vector_to_column_matrix([1 for _ in range(rows)])

    # define v vector
    v = matrix_subtraction(expected_returns, matrix_scalar_multiplication(vector_of_ones, risk_free_rate))

    # obtain the inverse of the covariance matrix
    cov_inv = inverse(covariance_matrix)

    # obtain coefficients for system of equations
    a = matrix_multiplication(transpose(vector_of_ones), matrix_multiplication(cov_inv, v))
    b = matrix_multiplication(transpose(vector_of_ones), matrix_multiplication(cov_inv, vector_of_ones))
    c = matrix_multiplication(transpose(v), matrix_multiplication(cov_inv, v))

    a = a[0][0]
    b = b[0][0]
    c = c[0][0]
    
    # solve system of equations
    lam1, lam2 = system_solver([[a, b], [c, a]], (2, 2))

    # substitute to get weigths vector w
    first_term = matrix_scalar_multiplication(matrix_multiplication(cov_inv, v), lam1/2)
    second_term = matrix_scalar_multiplication(matrix_multiplication(cov_inv, vector_of_ones), lam2/2)

    w = matrix_addition(first_term, second_term)
    return column_matrix_to_vector(w)


# ==================== Graphing volatilty against portfolio expected returns===============

# obtain a set of target returns (from 8% to 12%, in 1% intervals)
target_returns = [0.08 + 0.001 * i for i in range(41)]

# obtain volatility and portfolio expected returns for each target return
volatilites = []
portfolio_expected_returns = []
for i in range(len(target_returns)):
    w = optimal_weights_for_return(expected_returns, cov_mat, target_returns[i])
    x = math.sqrt(portfolio_variance(w, cov_mat)) # volatility is the square root of portfolio variance
    volatilites.append(x)

    y = portfolio_return(w, expected_returns)
    portfolio_expected_returns.append(y)

# plotting
plt.scatter(volatilites, portfolio_expected_returns, s = 10)
plt.title("Minimum-Variance Frontier")
plt.xlabel("Volatility")
plt.ylabel("Portfolio Expected Return")
plt.grid("True")
plt.savefig("efficient_frontier.png", dpi=300, bbox_inches="tight")
plt.show()
