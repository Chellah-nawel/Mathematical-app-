import numpy as np
from sympy import *

# fonction pour calculer la derive ou le gradient
def gradient(f, variables):
    result=[]
    for i in variables:
        derive= diff(f,i)
        result.append(derive)

    return np.array(result)


# descente de gradient
def gradient_descent(f, variables, start, alpha, tolerance):
    i=0

    grad = gradient(f, variables)

    # convertir f en fct numerique 
    grad_func = []
    for j in grad:
        grad_func.append(lambdify(variables, j))

    # les x0
    x = np.array(start, dtype=float)

    while (i<100):

        # valeur du gradient au point actuel
        grad_value = []
        for k in grad_func:
            grad_value.append(k(*x)) # * pour depiler le tableau

        grad_value = np.array(grad_value, dtype=float)

        xn = x - alpha * grad_value

        #condition d'arret
        erreur = np.linalg.norm(xn - x)
        if erreur < tolerance:
            break

        x=xn
        i+=1

    return x, erreur
