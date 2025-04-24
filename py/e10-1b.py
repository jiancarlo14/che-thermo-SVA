from math import exp
import sympy as sp
import numpy as np

PRESSURE = 70 #kPa

# Antoine Equation
A, B, C = sp.symbols("A, B, C")
T_expr = B / ( A - sp.ln(PRESSURE) ) + C 
T_i = sp.lambdify( (A, B, C), T_expr )

def T_(comp: int) -> float:
    if comp == 1:
        AA = 14.2724
        BB = 2945.47
        CC = 49.15
    elif comp == 2:
        AA = 14.2043
        BB = 2972.64
        CC = 64.15
    return T_i(AA, BB, CC)
# we have T_(1) and T_(2) the scope of the range

y = np.linspace(T_(1), T_(2), 100)
# the range which has 100 values

TT = sp.symbols("TT")
P_expr_ln = A - B / ( TT - C )
P_i_ln = sp.lambdify( (A, B, TT, C), P_expr_ln )

def P_(comp: int):
    if comp == 1:
        AA = 14.2724
        BB = 2945.47
        CC = 49.15
        pressures1 = []
        for temp in y:
            pressure1 = exp(P_i_ln(AA, BB, temp, CC))
            pressures1.append(pressure1)
        return pressures1
    elif comp == 2:
        AA = 14.2043
        BB = 2972.64
        CC = 64.15
        pressures2 = []
        for temp in y:
            pressure2 = exp(P_i_ln(AA, BB, temp, CC))
            pressures2.append(pressure2)
        return pressures2

x_1 = []
for p1, p2 in zip(P_(1), P_(2)):
    xx = ( PRESSURE - p2 ) / ( p1 - p2 )
    x_1.append(xx)
# this is the domain which has 100 values

x_2 = []
for p1, x1 in zip(P_(1), x_1):
    yy = ( p1 * x1 ) / PRESSURE
    x_2.append(yy)

# PLOT
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 18

t = []
for temp in y:
    celsius = temp - 273.15
    t.append(celsius)

plt.plot(x_1, t, label=r"$x_1$")
plt.plot(x_2, t, label=r"$y_1$")
plt.xlabel(r"$x_1, y_1$")
plt.ylabel(r"$t/\mathrm{^\circ C}$")
plt.legend()
plt.grid()
plt.show()
