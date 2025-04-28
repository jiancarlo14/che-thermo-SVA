import sympy as sp
from math import e, log

X1 = 0.85
X2 = 1 - X1
P = 101.33 # kPa
TOLERANCE = 1e-6

# Formula 1,2
t_var = sp.symbols("t_var")
def antoine_P(specie):
    if specie == 1:
        A = 16.59158
        B = 3643.31
        C = 33.424
        psati_formula = e**(A-B/(t_var-C))
    elif specie == 2:
        A = 14.25326
        B = 2665.54
        C = 53.424
        psati_formula = e**(A-B/(t_var-C))
    return psati_formula
a_formula = sp.lambdify(t_var, 2.771 - 0.00523*t_var)
alpha_formula = sp.lambdify(t_var, antoine_P(2)/antoine_P(1))

# Formula 3
a_var = sp.symbols("a_var")
def gamma(specie: int):
    if specie == 1:
        gm_formula = e**(a_var*X2)
    elif specie == 2:
        gm_formula = e**(a_var*X1)
    return gm_formula
gm1_formula = sp.lambdify(a_var,gamma(1))
gm2_formula = sp.lambdify(a_var,gamma(2))

# Formula 4
alpha_var, gm1_var, gm2_var = sp.symbols("alpha_var, gm1_var, gm2_var")
p1sat_formula = sp.lambdify((alpha_var, gm1_var, gm2_var), P/(X1*gm1_var + alpha_var*X2*gm2_var))

# Formula 5
p1sat_var = sp.symbols("p1sat_var")
A1 = 16.59158
B1 = 3643.31
C1 = 33.424
t_formula = sp.lambdify(p1sat_var, B1/(A1 - sp.log(p1sat_var, e)) - C1)

# Error Calc
t_new, t_old = sp.symbols("t_new, t_old")
error_formula = sp.lambdify((t_new, t_old), abs(t_new - t_old))

# Error Eval
error = sp.symbols("error")
no_error = error < TOLERANCE

# Initial Guess for T
def tisat_value(specie: int) -> float:
    if specie == 1:
        A = 16.59158
        B = 3643.31
        C = 33.424
        tisat = B/(A-log(P,e)) - C
    elif specie == 2:
        A = 14.25326
        B = 2665.54
        C = 53.424
        tisat = B/(A-log(P,e)) - C
    return tisat
t_now = X1*tisat_value(1) + X2*tisat_value(2)
print(t_now)

num_iter = 0
max_iter = 1000
no_error = False
while num_iter < max_iter:
    while not no_error:
        print("iteration #", num_iter)
        a_now = a_formula(t_now)   
        alpha_now = alpha_formula(t_now)
        gm1_now = gm1_formula(a_now)
        gm2_now = gm2_formula(a_now)
        p1sat_now = p1sat_formula(alpha_now, gm1_now, gm2_now)
        t_old = t_now
        t_now = t_formula(p1sat_now)
        error = error_formula(t_now, t_old)
        print("error =",error)
        print()
        if no_error:
            break
        else:
            num_iter += 1

