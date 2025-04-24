from math import exp
import sympy as sp 
import numpy as np

# (a) 
# Plot `P vs. x_1` 
# Plot `P vs. y_1` 
# t = 75 degrees Celsius

# Antoine Equation
A, B, C = sp.symbols("A, B, C")
Antoine_expr = A - B / (348.15 - C)
Antoine_rhs = sp.lambdify((A, B, C), Antoine_expr, 'numpy')

def Antoine(comp: int) -> float:
    if comp == 1:
        AA = 14.2724
        BB = 2945.47
        CC = 49.15
    elif comp == 2:
        AA = 14.2043
        BB = 2972.64
        CC = 64.15
    return Antoine_rhs(AA, BB, CC)

x1 = sp.symbols("x1")
P1sat = exp(Antoine(1))
P2sat = exp(Antoine(2))
P_total = sp.lambdify(x1, P1sat*x1 + P2sat*(1-x1), 'numpy')

a_h1 = np.linspace(0,1,100)
a_k = P_total(a_h1)
a_h2 = P1sat*a_h1/a_k

# PLOT
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 18

plt.plot(a_h1, a_k, label=r"$x_1$")
plt.plot(a_h2, a_k, label=r"$y_1$")
plt.xlabel(r"$x_1, y_1$")
plt.ylabel(r"$P/\mathrm{kPa}$")
plt.legend()
plt.grid()
plt.show()
