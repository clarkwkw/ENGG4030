#!/usr/bin/python
#
# Created by Albert Au Yeung (2010)
# http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python
# An implementation of matrix factorization
#
from __future__ import print_function
try:
    import numpy
    numpy.random.seed(1)
except:
    print("This implementation requires the numpy module.")
    exit(0)

###############################################################################

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in range(steps):
        newP, newQ = numpy.zeros(P.shape), numpy.zeros(Q.shape)
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        newP[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        newQ[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        P, Q = newP, newQ
        eR = numpy.dot(P,Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
    return P, Q.T

###############################################################################

if __name__ == "__main__":
    R = [
         [1, 1, 6, 4, 4, 0],
         [0, 3, 0, 4, 5, 4],
         [6, 0, 0, 2, 4, 4],
         [2, 1, 4, 5, 0, 5],
         [4, 4, 2, 0, 3, 1]
    ]
    TEST_R, TEST_C = 1, 2

    R = numpy.asarray(R)

    N = R.shape[0]
    M = R.shape[1]
    K = 2

    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)

    nP, nQ = matrix_factorization(R, P, Q, K)

    print("P:")
    print(nP)

    print("Q:")
    print(nQ)

    print("Prediction:", numpy.dot(nP[TEST_R, :], nQ.T[:, TEST_C]))
