import sympy as sp

A1, B1, C1 = 13.7819, 2726.81, 217.572
A2, B2, C2 = 13.9320, 3056.96, 217.625
P = 120
Y1 = 0.33
Y2 = 1 - Y1

t_var = sp.symbols("T")

def pisat_expr(specie: int) -> sp.Expr:
    if specie == 1:
        A, B, C = A1, B1, C1
    elif specie == 2:
        A, B, C = A2, B2, C2    
    return sp.exp(A - B/(t_var + C))

expr = Y1*P + (1 - Y1*P/pisat_expr(1))*pisat_expr(2) - P
d_expr = sp.diff(expr, t_var)

f = sp.lambdify(t_var, expr)
f_prime = sp.lambdify(t_var, d_expr)

num_iter = 0
MAX_ITER = 1000
t_prev = 100
error = 100
TOLERANCE = 1e-6

p1sat = sp.lambdify(t_var, pisat_expr(1))

while error > TOLERANCE and num_iter <= MAX_ITER:
    num_iter += 1
    print(f"iteration #{num_iter}")
    t_next = t_prev - f(t_prev)/f_prime(t_prev)
    error = abs(t_next - t_prev)
    print(f"error = {error}")
    print()
    
    if error <= TOLERANCE:
        print(f"T = {t_next} degrees Celsius")
        print(f"x_1 = {Y1*P/p1sat(t_next)}")
        break

    else:
        t_prev = t_next
