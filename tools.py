import numpy as np
import sympy as sp

x = sp.symbols("x")  

def negatif_signe(f, a, b, n=1000):
    if f(a)*f(b)<0:
        return True
    else:
        print("- pas de racine dans cette interval")
        return False

def continu(f,a,b):
    if a <= 0 <= b:
        #tester le point problm (en cas de div par 0)
        try:
            f(0)
        except:
            return False

    pts = np.linspace(a,b,1000)
    vals_y = f(pts)
    if np.any(np.isinf(vals_y)) or np.any(np.isnan(vals_y)):    #si un seul pt=NaN ou infini 
        print("-la fonction n'est pas continue")
        return False        #dicontinue
    else: return True       #continue

def precision (p):
    if p> 10**(-1) or p<0:
        print("-presicion trop grande")
        return False    
    else: return True

def check_x0(a,b,x0):
    if a<=x0 and x0<=b:
        return True
    else: 
        print("-x0 n'est pas dans [a,b]")
        return False 

#FOR FUNCTION HANDELING
def to_numpy(expr_str):
    expr_str = expr_str.replace("^", "**")
    expr = to_sympy(expr_str) #str to sympy
    return sp.lambdify(x, expr, "numpy") #str to sympy to numpy

def to_sympy(expr_str):#call in window
    expr_str = expr_str.replace("^", "**")
    return sp.sympify(expr_str)    #from str to sp

#expr est sympy
def sympyto_numpy(expr):
    return sp.lambdify(x, expr, "numpy")    #return as np

#f: en sympy
def deriver(f):
    return sp.diff(f, x)   #return as sympy
