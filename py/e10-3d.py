from math import e, log

from sympy import Expr, lambdify, symbols, ln

P = 101.33 # kPa
Y1 = 0.40
Y2 = 1 - Y1
TOLERANCE = 1e-6

def tisat_value(specie: int) -> float:
    if specie == 1:
        A = 16.59158
        B = 3643.31
        C = -33.424
    elif specie == 2:
        A = 14.25326
        B = 2665.54
        C = -53.424
    tisat = B/(A-log(P,e)) - C
    return tisat

T_INIT = tisat_value(1)*Y1 + tisat_value(2)*Y2

t_var = symbols("t_var")

a_formula = lambdify(t_var, 2.771 - 0.00523*t_var)

def pisat_expr(specie: int) -> Expr:
    if specie == 1:
        A = 16.59158
        B = 3643.31
        C = -33.424
    elif specie == 2:
        A = 14.25326
        B = 2665.54
        C = -53.424
    pisat = e**(A - B/(t_var+C))
    return pisat

p1sat_formula = lambdify(t_var, pisat_expr(1))
p2sat_formula = lambdify(t_var, pisat_expr(2))
alpha_formula = lambdify(t_var, pisat_expr(2)/pisat_expr(1))

p1sat_var, p2sat_var, gm1_var, gm2_var = symbols("p1sat_var, p2sat_var, gm1_var, gm2_var")
GM1_INIT = 1
GM2_INIT = 1

x1_formula = lambdify((p1sat_var, gm1_var), Y1*P/(gm1_var*p1sat_var))
x2_formula = lambdify((p2sat_var, gm2_var), Y2*P/(gm2_var*p2sat_var))

x1_var, x2_var, a_var = symbols("x1_var, x2_var, a_var")

gm1_formula = lambdify((x2_var, a_var), e**(a_var*x2_var**2))
gm2_formula = lambdify((x1_var, a_var), e**(a_var*x1_var**2))

alpha_var = symbols("alpha_var")

p1sat_formula2 = lambdify((gm1_var, gm2_var, alpha_var), P*(Y1/gm1_var + Y2/(gm2_var*alpha_var)))

A1 = 14.25326
B1 = 2665.54
C1 = -53.424

t_formula = lambdify(p1sat_var, B1/(ln(p1sat_var) - A1) - C1)

t_old, t_new = symbols("t_old, t_new")

error_formula = lambdify((t_old, t_new), abs(t_old - t_new))

error = 100
num_iter = 1
max_iter = 1000
t_now = T_INIT
gm1_now, gm2_now = GM1_INIT, GM2_INIT

# while num_iter < max_iter:
#     while error > TOLERANCE:
#         print(f"iteration #{num_iter}")
#         p1sat, p2sat = p1sat_formula(t_now), p2sat_formula(t_now)
#         alpha = alpha_formula(t_now)
#         x1 = x1_formula(p1sat, gm1_now,)
#         x2 = x2_formula(p2sat, gm2_now,)
#         a = a_formula(t_now)
#         gm1_new = gm1_formula(x2, a)
#         gm2_new = gm2_formula(x1, a)
#         p1sat_new = p1sat_formula2(gm1_new, gm2_new, alpha)
#         t_new = t_formula(p1sat_new)
#         error = error_formula(t_now, t_new)
#         print(f"error = {error}")
#         print()
#         if error <= TOLERANCE:
#             print(f"T = {t_new}")
#             print(f"x1 = {x1}")
#             print(f"x2 = {x2}")
#             break
#         else:
#             t_now = t_new
#             gm1_now, gm2_now = gm1_new, gm2_new
#             num_iter += 1


# TEST
t1sat = tisat_value(1)
t2sat = tisat_value(2)
# print(t1sat, t2sat)
# print(T_INIT)
a = a_formula(T_INIT)
p1sat = p1sat_formula(T_INIT)
p2sat = p2sat_formula(T_INIT)
alpha = alpha_formula(T_INIT)
# print(a, p1sat, p2sat, alpha)
x1 = x1_formula(p1sat, GM1_INIT)
x2 = x2_formula(p2sat, GM2_INIT)
# print(x1, x2)
gm1 = gm1_formula(x2, a)
gm2 = gm2_formula(x1, a)
# print(gm1, gm2)
p1sat_new = p1sat_formula2(gm1, gm2, alpha)
# print(p1sat_new, p1sat)
t_new = t_formula(p1sat_new)
print(f"T = {t_new}")
