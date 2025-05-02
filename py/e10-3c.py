import sympy as sp
from math import log, e

P = 101.33 # kPa
X1 = 0.85
X2 = 1 - X1
TOLERANCE = 1e-6

def antoine_ti(specie: int) -> float:
    if specie == 1:
        A = 16.59158
        B = 3643.31
        C = -33.424
    elif specie == 2:
        A = 14.25326
        B = 2665.54
        C = -53.424
    ti = B/(A - log(P, e)) - C
    return ti

T1SAT = antoine_ti(1)
T2SAT = antoine_ti(2)
# print(T1SAT)
# print(T2SAT)

T_INIT = X1*T1SAT + X2*T2SAT
# print(T_INIT)

# FORMULA 1, 2
t_var = sp.symbols("t_var")
a_formula = sp.lambdify(t_var, 2.771 - 0.00523*t_var)
def antoine_pi(specie: int) -> sp.Expr:
    if specie == 1:
        A = 16.59158
        B = 3643.31
        C = -33.424
    elif specie == 2:
        A = 14.25326
        B = 2665.54
        C = -53.424
    pi_expr = e**(A - B/(t_var + C))
    return pi_expr
alpha_formula = sp.lambdify(t_var, antoine_pi(2)/antoine_pi(1))
# print(a_formula(T_INIT))
# print(alpha_formula(T_INIT))

# FORMULA 3
a_var = sp.symbols("a_var")
def gm_expr(specie: int):
    if specie == 1:
        X = X2
    elif specie == 2:
        X = X1
    gm_formula = e**(a_var*X**2)
    return gm_formula
# print(gm_expr(1))
# print(gm_expr(2))
gm1_formula = sp.lambdify(a_var, gm_expr(1))
gm2_formula = sp.lambdify(a_var, gm_expr(2))
# print(gm1_formula(a_formula(T_INIT)))
# print(gm2_formula(a_formula(T_INIT)))
# gm1 = gm1_formula(a_formula(T_INIT))
# gm2 = gm2_formula(a_formula(T_INIT))
# alpha = alpha_formula(T_INIT)

# FORMULA 4
alpha_var, gm1_var, gm2_var = sp.symbols("alpha_var, gm1_var, gm2_var")
p1sat_formula = sp.lambdify((alpha_var, gm1_var, gm2_var), P/(X1*gm1_var + X2*gm2_var*alpha_var))
# print(p1sat_formula(alpha, gm1, gm2))
# p1sat = p1sat_formula(alpha, gm1, gm2)

# FORMULA 5
A1 = 16.59158
B1 = 3643.31
C1 = -33.424
p1sat_var = sp.symbols("p1sat_var")
t_formula = sp.lambdify(p1sat_var, B1/(A1 - sp.log(p1sat_var, e)) + C1)
# print(t_formula(p1sat))

# ERROR
def error(t_new, t_old) -> float:
    error = abs(t_new - t_old)
    return error
def check_error(error: float) -> bool:
    check_error = error <= TOLERANCE
    return check_error

# ITERATION
def solve():
    num_iter = 1
    max_iter = 1000
    no_error = False
    t_now = T_INIT

    while num_iter <= max_iter:
        while not no_error:
            print("iteration #",num_iter)
            alpha_new = alpha_formula(t_now)   
            a_new = a_formula(t_now)
            gm1_new = gm1_formula(a_new)
            gm2_new = gm2_formula(a_new)
            p1sat_new = p1sat_formula(alpha_new, gm1_new, gm2_new)
            t_new = t_formula(p1sat_new)
            error_now = error(t_new, t_now)
            no_error = check_error(error_now)
            print("error =",error_now)
            print()
            if no_error:
                print("T =", t_new)
                return (gm1_new, p1sat_new)
            else:
                num_iter += 1
                t_now = t_new

solve()
gm1, p1sat = solve()
# print(gm1, gm2)

y1 = X1*gm1*p1sat/P
print("y1 =", y1)
print("y2 =", 1-y1)
