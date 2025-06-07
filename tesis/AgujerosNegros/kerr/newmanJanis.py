# This is a Python script that implements the Newman-Janis algorithm, which takes a a set of tetrads withs a complex transformation to retun a new mwtric solution.
from sympy import *
r, theta, a, mass = symbols('r theta a m',real=True)

#Kronecker delta
def delta(i, j):
    return 1 if i == j else 0


# New null tetrads
def l(mu):
    return delta(mu, 1) 

def m(mu):
    return (1/(sqrt(2)*(r + I*a*cos(theta))))*(I*a*sin(theta)*(delta(mu, 0) - delta(mu, 1)) + delta(mu, 2) + (I /sin(theta))*delta(mu, 3))

def n(mu):
    return delta(mu,0)/2 - (1-(2*mass*(r- I*a*cos(theta)))/(r**2 +a**2*cos(theta)**2))*delta(mu,1)/8

def m_conjugate(mu):
    return m(mu).conjugate()

def metricComponent(mu, nu):
    return l(mu)*n(nu) +l(nu)*n(mu) - m(mu)*m_conjugate(nu) - m(nu)*m_conjugate(mu)

## This function returns in latex the metric tensor components for the Newman-Janis algorithm.
kerrMetric = [[latex(simplify(metricComponent(i, j))) for j in range(4)] for i in range(4)]

print("Metric tensor components for the Newman-Janis algorithm:")
print("\\begin{bmatrix}")
for i in range(4):
    row = " & ".join(kerrMetric[i])
    print(row + " \\\\")
print("\\end{bmatrix}")


