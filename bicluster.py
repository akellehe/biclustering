import numpy
import random
from intertools import combinations

# Get X
X = numpy.arange( 100 ).reshape( 10, 10 )

# Get m and n
m, n = X.shape # rows, columns

ITERATIONS_FOR_A = 1000

# Select initial k and l from {1...[m/2]} and {1...[n/2]} respectively (at random)
def get_k_and_l( ):
    k = random.randint( 1, int( m/2 ) )
    l = random.randint( 1, int( n/2 ) )
    return ( k, l )

# Start with a random B ( matrix of l cols )
def get_B_at_random( X, l, n ):
    l_zeros = numpy.zeros( ( 1, l ), dtype=int )
    l_rands = numpy.random.random( ( 1, l ) )
    l_rands *= n
    l_zeros += l_rands
    which_l_cols = l_zeros

    B = numpy.zeros( X.shape ) 
    for i in which_l_cols:
        B[:,i] = X[:,i]

    return B 

# Find the best A ( matrix of k rows ) for the chosen B
def get_A_candidate_at_random( X, k, m ):
    k_zeros = numpy.zeros( ( 1, k ), dtype=int )
    k_rands = numpy.random.random( ( 1, k ) )
    k_rands *= m
    k_zeros += k_rands
    which_k_rows = k_zeros 
   
    A = numpy.zeros( X.shape )
    for i in which_k_rows:
        A[i,:] = X[i,:]

    return A 

def sum_cols_of_A_over_rows_of_B( A, B, X ):
    C = A * B
    indicies = C.nonzero( )
    entries = A[ indicies ]
    total = numpy.sum( entries )
    return total

def get_initial_A( k, l, B, X ):
    running_max = 0
    winner = None
    for iteration in range( 0, ITERATIONS_FOR_A ):
        A = get_A_candidate_at_random( X, k, m )
        total = sum_cols_of_A_over_rows_of_B( A, B, X )
        if total > running_max:
            running_max = total
            winner = A
    return winner

def have_converged( A, B ):
    return sum( A - B ) == 0

def build_matrix_from_k_rows_of_X( k_rows, X ):
    M = numpy.zeros( X.shape )
    for row in k_rows:
        M[row,:] = X[row,:]
    return M

def build_matrix_from_l_cols_of_X( l_cols, X ):
    M = numpy.zeros( X.shape )
    for col in l_cols:
        M[:,col] = X[:,col]
    return M

def sum_rows_of_A_over_cols_of_B( A, B ):
    print "Do it."

def sum_cols_of_B_over_rows_of_A( A, B ):
    print "Yep"

def get_k_rows_with_largest_sum_over_columns_of_B( k, B ):
    column_list = range( 1, m )
    winning_total = 0
    winner = None
    for max_candidate in combinations( column_list, k ):
        A = build_matrix_from_k_rows_of_X( max_candidate, X )
        score = sum_rows_of_A_over_cols_of_B( A, B )
        if score > winning_total:
            winner = A
            winning_total = score
    return A


def get_l_columns_with_largest_sum_over_rows_of_A( l, A ):
    row_list = range( 1, n )
    winning_total = 0
    winner = None
    for max_candidate in combinations( row_list, l ):
        B = build_matrix_from_l_cols_of_X( max_candidate, X )
        score = sum_cols_of_B_over_rows_of_A( A, B )
        if score > winning_total:
            winner = B
            winning_total = score
    return B

B = get_B_at_random( )
A = get_initial_A( k, l, B, X )
while have_converged( A, B ) == False:
    A = 
    B = 


