import sympy as sp
from math import e
from typing import Tuple
import importlib

module = importlib.import_module("e10-3a")
P1SAT = module.P1SAT
P2SAT = module.P2SAT
CONST = module.CONST

Y1 = 0.6
Y2 = 1-Y1
TOLERANCE = 1e-6

# Formula 1
gm1_var, gm2_var = sp.symbols("gm1_var, gm2_var")
p_formula = sp.lambdify((gm1_var, gm2_var), 1/(Y1/(gm1_var*P1SAT) + Y2/(gm2_var*P2SAT)))

# Formula 2
p_var = sp.symbols("p_var")
x1_formula = sp.lambdify((p_var, gm1_var), Y1*p_var/gm1_var/P1SAT)

# Formula 3
x1_var, x2_var = sp.symbols("x1_var, x2_var")
gm1_formula = sp.lambdify(x2_var, e**(CONST*x2_var**2))
gm2_formula = sp.lambdify(x1_var, e**(CONST*x1_var**2))

def p_solve(gm1, gm2) -> float:
    p_value = p_formula(gm1, gm2)
    return p_value

def x1_x2_solve(p, gm1) -> Tuple[float, float]:
    x1 = x1_formula(p, gm1)
    x2 = 1 - x1
    return (x1, x2)

def gm1_gm2_solve(x1, x2) -> Tuple[float, float]:
    gm1 = gm1_formula(x2)
    gm2 = gm2_formula(x1)
    return (gm1, gm2)

def error_solve(x1_now, x1_prev) -> float:
    error = x1_now - x1_prev
    return error

def check_error(error) -> bool:
    no_error = error <= TOLERANCE
    return no_error


gm1_now = 1
gm2_now = 1
num_iter = 0
max_iter = 1000
error = 100
x1_prev = 0

while num_iter <= max_iter:
    while error >= TOLERANCE:
        p_now = p_solve(gm1_now, gm2_now)
        print("iteration #",num_iter)
        x1_now, x2_now = x1_x2_solve(p_now, gm1_now)
        error = error_solve(x1_now, x1_prev)
        print("error =", error)
        print()
        no_error = check_error(error)
        if no_error:
            print("P =", p_now)
            print("x1 =", x1_now)
            print("x2 =", x2_now)
            break
        else:
            gm1_now, gm2_now = gm1_gm2_solve(x1_now, x2_now)
            num_iter += 1
            x1_prev = x1_now
