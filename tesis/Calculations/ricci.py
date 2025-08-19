from christoffel import Christoffel_all # importar el programa anterior
from sympy import *

t, r, theta, phi, = symbols('t r theta phi') 

indices = [t, r, theta, phi]

# Lista con los simbolos de Christoffel
Christoffel_symbols = Christoffel_all()


# Por definicion el tensor de Ricci es la contraccion de 2 indices del tensor de Riemann

# mu , nu siendo los indices del Ricci
for mu in range(0,4,1):
    for nu in range(0,4,1):
        ricci_mu_nu = 0
        ##sobre el indice mudo alpha
        for alpha in range(0,4,1):
            ricci_mu_nu += diff(Christoffel_symbols[alpha][mu][nu],indices[alpha]) -diff(Christoffel_symbols[alpha][mu][alpha],indices[nu]) 
            # indice mudo lambda
            for lam in range(0,4,1):
                ricci_mu_nu +=  Christoffel_symbols[alpha][alpha][lam]*Christoffel_symbols[lam][mu][nu] - Christoffel_symbols[alpha][nu][lam]*Christoffel_symbols[lam][mu][alpha]
        ricci_mu_nu = cancel(ricci_mu_nu)
        ricci_mu_nu = simplify(ricci_mu_nu)
 
        # imprimir en pantalla los componentes no cero
        if ricci_mu_nu != 0:
            print(f"R_{{{mu}{nu}}} &= {latex(ricci_mu_nu)} \\\\")