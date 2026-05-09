import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from tools import *
#ALGO NEWTON RAPHSON

#df= f'(x) ddf=f''(x)
def verifie_converge(f, a, b, df, ddf):

    if negatif_signe(f,a,b)== False: #pas de racine dans l interval
        return False

    cond1= (f(a)*f(b) < 0)      #tvi negatif_signe

    x = np.linspace(a, b, 100)

    cond2 = np.all(df(x) != 0)                          #assurer la monotonie de f dans [a,b]
    cond3 = (np.all(ddf(x) > 0) or np.all(ddf(x) < 0))  # Condition sur la dérivée seconde qu'elle garde le même signe dans [a,b]

    #c = x[np.argmin(np.abs(df(x)))]
    c = min([abs(df(xi)) for xi in x])      #c = min(f'(a), f'(b))
    cond4 = (abs(f(c) / df(c)) <= (b - a))  #|f(c)/f'(c)|< b-a 

    if(cond1 and cond2 and cond3 and cond4):
        return True
    else:
        print("l'algo de newton ne converge pas")
        return False


# f:function (en str) [a,b] ep:precision (d'erreur) x0:point de depart
def newton_r(f,a,b,x0,ep):

    if continu(to_numpy(f),a,b) == False:
        return None,0

    if check_x0(a,b,x0)==False:
        return None,0
    
    if precision(ep) == False:
        return None,0

    maxi=100               #max iteration
    x= x0
    
    f_sym = to_sympy(f)
    df_sym= deriver(f_sym)          #f'(x) en sp
    ddf_sym= deriver(df_sym)              #f''(x) en sp

    df= sympyto_numpy(df_sym)    #f' est en np
    ddf=sympyto_numpy(ddf_sym)  #f'' est en np
    f=to_numpy(f)               # en np pour verifier cv

    #majoree l erreur
    m= np.inf               #+ infini
    M=-np.inf               #- infini
    x_range = np.linspace(a, b, 100)
    df_vals = df(x_range)    
    ddf_vals = ddf(x_range)

    m=np.min(np.abs(df_vals) )     #born inf f'
    M=np.max(np.abs(ddf_vals))      #born sup f''

    row=[]
    iteration=[x]
    err=[]
    xnext = x0 
    if(verifie_converge(f, a, b, df, ddf)== True):
        
        for i in range(maxi):   
            xnext= x - f(x)/df(x)                                      #xnext is xn+1 -> xn+1= xn - f(xn) / f'(xn)
            err_pr = abs(xnext - x)                                    #erreur pratic -> |xn+1- xn|
            error = (M / (2*m))* err_pr**2 if m != 0 else np.inf       #error theo (if to avoid div 0)

            row.append([i,f"{x:.7f}",f"{f(x):.7f}", f"{error:.7f}"])
            err.append(error)                    #store in array
            x= xnext            
            iteration.append(x)


            if error < ep:                      #cond d arret erreur estimer < epsilon
                break

    else: return  None,0                        #La suite ne converge pas, on ne peut pas appliquer l'algo de Newton

    draw_table(row)
    graphe(f,a,b,iteration, x0,xnext)
    return xnext, i+1      #return racine et nbr iteration
    

def draw_table(row):
    cols = ["Iteration","x", "f(xn)", "Erreur"]                         #les colonnes
    fig,ax = plt.subplots(figsize=(9, 6))                               #to position
    ax.axis('off')                                                      #to hide x y its not a graphe 
    ax.table(cellText=row, colLabels=cols, loc='center')                #insert vals
    plt.title("Algo Newton Ralphson", fontsize=13, fontweight='bold')
    plt.savefig('resultat/newtonR_table.png', dpi=300, bbox_inches='tight')

def graphe(f,a,b,iteration, x0,racine):
    x_plot = np.linspace(a, b, 500)
    plt.figure()
    plt.plot( x_plot , f(x_plot), color="black",linewidth=1)

    plt.scatter( iteration , [f( xi) for xi in iteration ] ,label =f'iteration x0={x0}')    #voir les iteration de newton
    plt.scatter(racine, f(racine), color='red', label=f'racine = {racine:.5f}')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.axhline (0 , color ="black", linewidth =0.5)    #les x
    plt.axvline (0 , color ="black", linewidth =0.5)    #les y
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig('resultat/newtonR_graphe.png', dpi=300, bbox_inches='tight')
