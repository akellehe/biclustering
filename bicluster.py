'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import numpy
import random
import operator
import time
from math import *

#A, k, m rows
#B, l, n cols

ITERATIONS = 1000
SIZE = 200
SHAPE = ( SIZE, SIZE )

# Populate a test matrix with gaussian noise in (0,1)
X = numpy.random.normal( size=SHAPE )
X += 2
X *= 0.5

# Add a feature to detect
FEATURE = numpy.zeros( SHAPE )
FEATURE[0:SIZE/2,0:SIZE/2] = 4
X += FEATURE

print X

m, n = X.shape

# Select initial k and l from {1...[m/2]} and {1...[n/2]} respectively (at random)
def get_k_and_l( m, n ):
    k = random.randint( 1, int( m/2 ) )
    l = random.randint( 1, int( n/2 ) )
    return ( k, l )


def get_initial_B( l, n, X ):
    l_zeros = numpy.zeros( ( 1, l ), dtype=int )
    l_rands = numpy.random.random( ( 1, l ) )
    l_rands *= n
    l_zeros += l_rands
    which_l_cols = l_zeros
    B = numpy.zeros( X.shape )
    for i in which_l_cols:
        B[:,i] = X[:,i]
    return B

def get_k_rows_with_largest_sum_over_B( k, B ):
    sums = [ ]
    for row in B:
        sums.append( sum( row ) )

    best_rows = [ ]
    # Row indicies sorted lowest to highest:
    inds = [ i for ( i, j ) in sorted( enumerate( sums ), key = operator.itemgetter( 1 ) ) ]
    for i in range( 0, k ):
        best_rows.append( inds.pop( ) )

    return best_rows

def get_A_from_row_indicies( rows, X ):
    A = numpy.zeros( X.shape )
    for row_index in rows:
        A[row_index,:] = X[row_index,:]
    return A

def get_l_cols_with_largest_sum_over_A( l, A ):
    sums = [ ]
    for col in A.transpose( ):
        sums.append( sum( col ) )

    best_cols = [ ]
    # Col indicies sorted from lowest to highest:
    inds = [ i for ( i, j ) in sorted( enumerate( sums ), key = operator.itemgetter( 1 ) ) ]
    for i in range( 0, l ):
        best_cols.append( inds.pop( ) )

    return best_cols

def get_B_from_col_indicies( cols, X ):
    B = numpy.zeros( X.shape )
    for col_index in cols:
        B[:,col_index] = X[:,col_index]
    return B

def have_converged( newA, newB, oldA, oldB ):
    a_converged = ( sum( oldA ) - sum( newA ) ).all( ) == 0 
    b_converged = ( sum( oldB ) - sum( newB ) ).all( ) == 0 
    if a_converged and b_converged:
        return True
    else:
        return False
   
def get_intersection( A, B ):
    intersection = numpy.zeros( A.shape )
    C = A * B
    indicies = C.nonzero( )
    intersection[ indicies ] = A[ indicies ]
    return intersection

def binomial( n, k ):
    if n > k:
        b = factorial( n ) / ( factorial( k ) * factorial( n - k ) )
        return b

def S( U, k, l, m, n ):
    tau = numpy.average( U )

    first_term  = -log( binomial( m, k ) * binomial( n, l ), 2 )
    second_term = ( ( tau**2.0 ) * k * l ) / ( 2.0 * log( 2.0 ) )
    third_term  = -log( ( tau**2.0 * k * l ), 2 ) / 2.0

    return log( 2.0 ) * ( first_term + second_term + third_term ) 

def get_remaining_time( start_time, total_time, iteration ):
    if iteration == 0:
        return ""
    elapsed_time = total_time - start_time
    time_per_iteration = elapsed_time / iteration
    return str( time_per_iteration * ( ITERATIONS - iteration ) / 60 ) + " minutes remaining"

if __name__ == '__main__':
    winner = numpy.zeros( X.shape )
    winning_score = 0 
    end_time = False
    start_time = time.time( )
    for it in range( 0, ITERATIONS ):
        k, l = get_k_and_l( m, n )
        B = get_initial_B( l, n, X )
        lastA = numpy.zeros( X.shape )
        lastB = numpy.zeros( X.shape )
        while True: 
            a_inds = get_k_rows_with_largest_sum_over_B( k, B )
            A = get_A_from_row_indicies( a_inds, X )
            b_inds = get_l_cols_with_largest_sum_over_A( l, A )
            B = get_B_from_col_indicies( b_inds, X )
            if have_converged( A, B, lastA, lastB ):
                break
            lastA = A.copy( )
            lastB = B.copy( )
        U = get_intersection( A, B )
        U_score = S( U, k, l, m, n )
        if U_score > winning_score:
            winner = U.copy( )
            winning_score = U_score

        print get_remaining_time( start_time, time.time( ), it )


    print winning_score
    print winner
