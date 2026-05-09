import numpy as np
import matplotlib.pyplot as plt
from tools import *

#ALGO DICHOTOMIE

# f function (en str) [a,b] p precision
def dichotomie(f, a, b, p):
    f=to_numpy(f)
    i=0                     #iteration
    a1=a                    #new interval
    b1=b
    error=(b-a)             #erreur initial = 2^0  
    m= (a1 + b1)/2          #initialisation in case we dont get into while
    row=[]                  #store results for table
    
    if precision (p)== False:
        return None, None

    if continu(f,a,b)== False:
        return None, None

    if negatif_signe(f,a,b)== False:
        return None, None
    
    else: #f(a)*f(b)<0 
        while (error > p):
            m= (a1 + b1)/2                  #middle 
            error=(b-a)/2**(i+1)            #erreur theo (l interval est div a chque fois en 2)
            i=i+1 
            row.append([i, f"{m:.7}", f"[{a1:.7f}, {b1:.7f}]", f"{error:.7f}"])

            if(f(a1)*f(m)<0):   # racine in [a,m]
                b1=m            #changer b
            else:               # racine in [m,b]
                a1=m            #changer a
                
            if f(m)==0: break

        draw_table(row)
        graph(f,row,m,a,b)
        return m, i         #return racine and nbr iteration
    

def draw_table(row):
    cols = ["Itération", "Solution m", "Intervalle [a, b]", "Erreur"]   #les colonnes
    fig,ax = plt.subplots(figsize=(9, 6))                               #to position
    ax.axis('off')                                                      #to hide x y its not a graphe 
    ax.table(cellText=row, colLabels=cols, loc='center')                #insert vals
    plt.title("Methode de Dichotomie", fontsize=13, fontweight='bold')
    plt.savefig('resultat/dichotomie_table.png', dpi=300, bbox_inches='tight')

def graph(f,row,racine,a,b):
    x = np.linspace(a, b, 500)                              #interval de dessin de funct
    plt.figure()                                            #create new window
    plt.plot(x, f(x), color='black', linewidth=1)           #draw funct
    plt.axhline(0, color='black', linewidth=0.5)            #les x
    plt.axvline(0, color='black', linewidth=0.5)            #les y
    plt.vlines(x=a, ymin=0, ymax=f(a), colors='red', linewidth=0.7, linestyle='--', label='Interval')
    plt.vlines(x=b, ymin=0, ymax=f(b), colors='red', linewidth=0.7, linestyle='--')
    plt.scatter(a, 0,marker='+',color='red')
    plt.scatter(b, 0,marker='+',color='red')
    plt.scatter([float(r[1]) for r in row],[f(float(r[1])) for r in row],marker='+',linewidth=0.7, color='blue',label='Iterations')
    plt.scatter(racine, f(racine), marker='*' ,color='green',label=f'racine ≈ {racine:.5f}')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Dichotomie - graphe",fontsize=12, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig('resultat/dichotomie_graphe.png', dpi=500, bbox_inches='tight')
