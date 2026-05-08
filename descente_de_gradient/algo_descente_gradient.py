import numpy as np
import matplotlib.pyplot as plt
from sympy import *

# fonction pour calculer la derive ou le gradient
def gradient(f, variables):
    result=[]
    for i in range(variables):
        derive= diff(f,i)
        result.append(derive)

    return np.array(result)