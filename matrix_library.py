import copy

# a matrix is represented by a list of lists
# for matrix[i][j], i is row number and j is column number

def matrix_input():
    while True:
        try:
            no_of_rows = int(input(f"How many rows are in your matrix? "))
            if no_of_rows <= 0:
                print("ERROR! Number of rows must be a positive integer")
            else: break
        except ValueError:
            print("ERROR! Number of rows must be a positive integer")
    while True:
        try:
            no_of_columns = int(input(f"How many columns are in your matrix? "))
            if no_of_columns <= 0:
                print("ERROR! Number of columns must be a positive integer")
            else: break
        except ValueError:
            print("ERROR! Number of columns must be a positive integer")
    matrix = []
    for i in range(no_of_rows):
        row = []
        for j in range(no_of_columns):
            while True:
                try:
                    x = float(input(f"Enter the entry on row {i+1} and column {j+1}: "))
                    row.append(x)
                    break
                except ValueError:
                    print(f"ERROR! Input for matrix must be a number")
        matrix.append(row)
    return matrix

# gets the shape of a matrix. Format is m x n, where m is number of rows and n is number of columns 
def matrix_shape(matrix):
    no_of_rows = len(matrix)
    no_of_columns = len(matrix[0])
    return (no_of_rows, no_of_columns)

# makes a copy of the matrix
def matrix_copy(matrix):
    return copy.deepcopy(matrix)

# matrix addition
def matrix_addition(mat_1, mat_2):
    result = []
    if matrix_shape(mat_1) != matrix_shape(mat_2):
        print(f"ERROR! Matrices should be of the same dimensions")
    else:
        no_of_rows, no_of_columns = matrix_shape(mat_1)
        for i in range(no_of_rows): # for each row
            row = []
            for j in range(no_of_columns): # for each column in each row, i.e. for each element
                x = mat_1[i][j] + mat_2[i][j]
                row.append(x)
            result.append(row)
        return result
    
# matrix subtraction
def matrix_subtraction(mat_1, mat_2):
    result = []
    if matrix_shape(mat_1) != matrix_shape(mat_2):
        print(f"ERROR! Matrices should be of the same dimensions")
    else:
        no_of_rows, no_of_columns = matrix_shape(mat_1)
        for i in range(no_of_rows): # for each row
            row = []
            for j in range(no_of_columns): # for each column in each row, i.e. for each element
                x = mat_1[i][j] - mat_2[i][j]
                row.append(x)
            result.append(row)
        return result

# matrix multiplication
# for A*B to be valid, if A is m x n and B is p x q, then n = p 
def matrix_multiplication(mat_1, mat_2):
    result = []
    rows_mat_1, columns_mat_1 = matrix_shape(mat_1)
    rows_mat_2, columns_mat_2 = matrix_shape(mat_2)

    if columns_mat_1 != rows_mat_2:
        print(f"ERROR! Matrices do not have compatible dimensions to multiplied")
    else:
        for i in range(rows_mat_1): # for each row in matrix 1
            row = []
            for j in range(columns_mat_2): #for column in matrix 2
                x = 0
                for k in range(columns_mat_1):
                    x += mat_1[i][k] * mat_2[k][j]
                row.append(x)
            result.append(row)
        return result
 
# matrix scalar multiplication
def matrix_scalar_multiplication(matrix, scalar):
    no_of_rows, no_of_columns = matrix_shape(matrix)
    result = []
    for i in range(no_of_rows):
        row = []
        for j in range(no_of_columns):
            x = matrix[i][j] * scalar
            row.append(x)
        result.append(row)
    return result
         
# transpose of matrix (matrix can have any dimensions)
def transpose(matrix):
    no_of_rows, no_of_columns = matrix_shape(matrix)
    result = []
    for i in range(no_of_columns): # i is index for column
        row = []
        for j in range(no_of_rows): # j is index for row 
            x = matrix[j][i] #instead of going by row then column, we go by column then row 
            row.append(x)
        result.append(row)
    return result

# convert a vector to matrix form (column matrix)
def vector_to_column_matrix(vector):
    result = []
    for i in vector:
        row = []
        row.append(i)
        result.append(row)
    return result

# convert a column matrix to a vector
def column_matrix_to_vector(matrix):
    no_of_rows, no_of_columns = matrix_shape(matrix)
    if no_of_columns != 1:
        print(f"ERROR! Matrix should be a column matrix")
    else:
        result = []
        for i in range(no_of_rows):
            x = matrix[i][0]
            result.append(x)
        return result

# multiplication between vector and matrix
def matrix_vector_multiplication(matrix, vector):
    #convert vector to matrix form 
    vector_in_matrix_form = vector_to_column_matrix(vector)
    intermediate = matrix_multiplication(matrix, vector_in_matrix_form)
    #convert the result matrix (intermediate) to vector form
    return column_matrix_to_vector(intermediate)

#===============GAUSSIAN ELIMINATION===============
# row operations
def row_swap(matrix, row_1, row_2): #rows are integers
    rows, columns = matrix_shape(matrix)
    i = row_1 - 1 # original index of row 1
    j = row_2 - 1 # original index of row 2
    matrix[i], matrix[j] = matrix[j], matrix[i]
    return matrix

# multiplying a row by a scalar
def row_scaling(matrix, row_1, scalar):
    i = row_1 - 1 # index of row
    rows, columns = matrix_shape(matrix)
    scaled_row = []
    for j in range(columns):
        x = matrix[i][j] * scalar
        scaled_row.append(x)
    matrix[i] = scaled_row
    return matrix

# row addition (e.g. R1 -> R1 + kR2, where k is a constant)
def row_addition(matrix, row_1, row_2, scalar):
    i = row_1 - 1 # index of row 1
    j = row_2 - 1 # index of row 2
    rows, columns = matrix_shape(matrix)
    updated_row = []
    for s in range(columns):
        x = matrix[i][s] + scalar * matrix[j][s]
        updated_row.append(x)
    matrix[i] = updated_row
    return matrix

# RREF
def RREF(matrix):
    temp = matrix_copy(matrix)
    rows, columns = matrix_shape(matrix)
    pivot_row_index = 0
    pivot_column_index = 0

    while pivot_row_index <= (rows-1) and pivot_column_index <= (columns-1): #stops once indices are outside matrix 
        pivot = temp[pivot_row_index][pivot_column_index]
        if pivot != 0:
            row_scaling(temp, pivot_row_index + 1, 1/pivot)
            for j in range(rows):
                if j == pivot_row_index:
                    continue
                row_addition(temp, j+1, pivot_row_index+1, -temp[j][pivot_column_index])
            #move a row down and a column right
            pivot_row_index += 1 
            pivot_column_index += 1
        else: # pivot = 0
            found_pivot = False
            for k in range(pivot_row_index+1, rows):
                if temp[k][pivot_column_index] != 0:
                    row_swap(temp, k+1, pivot_row_index+1)
                    found_pivot = True
                    break
                #else keep searching for non zero entries
            if found_pivot == False:
                #only move to next column
                pivot_column_index += 1
    return temp

# reduced echelon form
def REF(matrix):
    temp = matrix_copy(matrix)
    rows, columns = matrix_shape(matrix)
    pivot_row_index = 0
    pivot_column_index = 0

    swap_count = 0

    while pivot_row_index <= (rows-1) and pivot_column_index <= (columns-1): #stops once indices are outside matrix 
        pivot = temp[pivot_row_index][pivot_column_index]
        if pivot != 0:
            for j in range(pivot_row_index+1, rows):
                if j == pivot_row_index:
                    continue
                row_addition(temp, j+1, pivot_row_index+1, -(temp[j][pivot_column_index])/(temp[pivot_row_index][pivot_column_index]))
            #move a row down and a column right
            pivot_row_index += 1 
            pivot_column_index += 1
        else: # pivot = 0
            found_pivot = False
            for k in range(pivot_row_index+1, rows):
                if temp[k][pivot_column_index] != 0:
                    row_swap(temp, k+1, pivot_row_index+1)
                    swap_count += 1
                    found_pivot = True
                    break
                #else keep searching for non zero entries
            if found_pivot == False:
                #only move to next column
                pivot_column_index += 1
    return temp, swap_count

# determinant for square matrix
def det(matrix):
    temp, swap_count = REF(matrix)
    rows, columns = matrix_shape(matrix)
    
    if rows != columns:
        print("Determinant does not exist as matrix is not square")
    else:
        if swap_count % 2 == 0:
            swap_count = 1
        else:
            swap_count = -1
        x = 1
        for i in range(rows):
            x *= temp[i][i]
        x *= swap_count
        return x
    
# inverse of a matrix
def inverse(matrix):
    rows, columns = matrix_shape(matrix)
    if rows != columns:
        print(f"Matrix is non-invertible as it is not a square matrix")
    elif det(matrix) == 0:
        print(f"Matrix is non-invertible as its determinant is zero")
    else: 
        #generate identity matrix with dimensions same as that of the matrix
        identity_matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                if i == j:
                    x = 1
                    row.append(x)
                else: 
                    x = 0
                    row.append(x)
            identity_matrix.append(row)
        augmented_matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                if j != columns - 1:
                    x = matrix[i][j]
                    row.append(x)
                else:
                    x = matrix[i][j]
                    row.append(x)
                    for k in range(columns):
                        x = identity_matrix[i][k]
                        row.append(x)
            augmented_matrix.append(row)
        
        # get the augmented matrix after RREF is complete
        inverse_augmented_matrix = RREF(augmented_matrix)
        
        augmented_rows, augmented_columns = matrix_shape(inverse_augmented_matrix)
        inverse_matrix = []
        for i in range(rows):
            row = []
            for j in range(columns, augmented_columns):
                x = inverse_augmented_matrix[i][j]
                row.append(x)
            inverse_matrix.append(row)
        return inverse_matrix

# rank of a matrix
def rank(matrix):
    rref_matrix = RREF(matrix)
    rows, columns = matrix_shape(matrix)
    zero_rows = 0
    for i in range(rows):
        status = all(abs(rref_matrix[i][j]) < 1e-12 for j in range(columns))
        if status == True:
                zero_rows += 1
    rank = rows - zero_rows
    return rank

def pivot_column_index_finder(matrix):
    rows, columns = matrix_shape(matrix)
    pivot_column_indices = []
    free_variable_column_indices = []

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == 0:
                pass
            else:
                pivot_column_indices.append(j)
                break
        
    return pivot_column_indices

# linear system of equations solver
def system_solver(matrix, constant_vector):
    b = vector_to_column_matrix(constant_vector)
    temp = matrix_copy(matrix)
    rows, columns = matrix_shape(matrix)

    # forms the augmented matrix A|b
    augmented_matrix = []
    for i in range(rows):
        row = []
        row = temp[i]
        row.append(b[i][0])
        augmented_matrix.append(row)
    
    #Carry out RREF on augmented matrix
    result_matrix = RREF(augmented_matrix)

    #check if system is consistent or inconsistent
    if rank(matrix) != rank(result_matrix):
        print(f"System is inconsistent")
        return None
    else: pass

    pivot_column_indices = pivot_column_index_finder(result_matrix)
    free_variable_column_indices = []

    for i in range(columns):
        if i in pivot_column_indices:
            pass
        else:
            free_variable_column_indices.append(i)


    number_of_pivots = len(pivot_column_indices)
    number_of_free_variables = len(free_variable_column_indices)

    '''print(f"pivot columns: {pivot_column_indices}, free columns: {free_variable_column_indices}")'''

    #check if system has infinite solutions or a unique solution
    # infinite solutions if (variables > rank)
    if number_of_pivots + number_of_free_variables != rank(result_matrix):
        # find particular solution
        particular_solution = []
        for i in range(rows):
            x = result_matrix[i][columns]
            particular_solution.append(x)

        # find direction vectors by solving Ax = 0
        null_space_basis = []

        for i in free_variable_column_indices:
            result_copy = matrix_copy(result_matrix)
            '''print(f"variable in column {i} is not 0")'''
            # make all other free variables equal to 0
            for j in range(rows):
                for k in free_variable_column_indices:
                    if k == i:
                        pass
                    else:
                        result_copy[j][k] = 0
            '''print(result_copy)'''    
            direction_vector = []
            for t in range(rows):
                if t == i:
                    x = 1.0
                else:
                    x = - result_copy[t][i]
                direction_vector.append(x)
            null_space_basis.append(direction_vector)
        return {
            "particular solution": particular_solution,
            "Direction vectors": null_space_basis
        }
    else: pass

    answers = []
    for i in range(rows):
        x = result_matrix[i][columns]
        answers.append(x)
    return answers

# dot product
def dot_product(vct_1, vct_2):
    if len(vct_1) != len(vct_2):
        print("Error! Vectors must be of the same length")
        return None
    else:
        x = 0
        for i in range(len(vct_1)):
            x += vct_1[i] * vct_2[i]
        return x
