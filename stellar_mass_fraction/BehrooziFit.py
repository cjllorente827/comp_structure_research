import numpy as np

nu = lambda a : np.exp(-4*a*a)

eps0 = -1.777
epsa = -0.006
epsz = -0.000
eps2 = -0.119
eps = lambda z, a: 10**( eps0 + (epsa*(a-1) +(epsz)*z)*nu(a) + eps2*(a-1) )

M10 = 11.514
M1a = -1.793
M1z = -0.251
M_1 = lambda z, a: 10**( M10 + (M1a*(a-1) + M1z*z)*nu(a) )

alph0 = -1.412
alpha = 0.731
alph = lambda a: alph0 + alpha*(a-1)*nu(a)

delt0 = 3.508
delta = 2.608
deltz = -0.043
delt = lambda z, a: delt0 + (delta*(a-1) + deltz*z)*nu(a) 

gamm0 = 0.316
gamma = 1.319
gammz = 0.279
gamm = lambda z, a: gamm0 + (gamma*(a-1) + gammz*z)*nu(a) 

#############################################################################
# Returns the median stellar mass of a halo for a given stellar mass and
# redshift according to a fit function described in Behroozi & Weschler 2013
#############################################################################
def stellar_mass(Mh, z):

    a = 1/(1+z)
    E = eps(z,a)
    M = M_1(z,a)
    A = alph(a)
    D = delt(z,a)
    G = gamm(z,a)
    
    f = lambda x : -np.log10(10**(A*x)+1) + D * (np.log10(1+np.exp(x)))**G / (1+np.exp(10**(-x)))
    
    M_s = 10**( np.log10(E*M) + f(np.log10(Mh/M)) - f(0) )
    return M_s
