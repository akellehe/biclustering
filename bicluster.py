import numpy
import random

# Get X
X = arange( 100 ).reshape( 10, 10 )

# Get m and n
m, n = X.shape( ) # rows, columns

# Select initial k and l from {1...[m/2]} and {1...[n/2]} respectively (at random)
def get_k_and_l( ):
    k = random.randint( 1, m )
    l = random.randint( 1, n )
    return ( k, l )

# Start with a random B
def get_B_at_random( X ):
    l_zeros = numpy.zeros( ( 1, l ), dtype=int )
    l_rands = numpy.random.random( ( 1, l ) )
    l_rands *= l
    l_rands += l_zeros
    which_l_rows = l_rands

    B = numpy.zeros( X.shape( ) ) 
    for i in which_l_rows:
        B[i,:] = X[i,:]

    return B 

# Find the best A for the chosen B
def find_optimal_A( k, l, X ):
    k_zeros = numpy.zeros( ( 1, k ), dtype=int )
    k_rands = numpy.random.random( ( 1, k ) )
    k_rands *= k
    k_rands += k_zeros
    which_k_rows =  k_rands
    
    k_rows = X[ which_k_rows ]



def sum_cols_of_A_over_rows_of_B( A, B ):
    
