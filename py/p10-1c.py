import sympy as sp

t_var = sp.symbols("T")

A1, B1, C1 = 13.7819, 2726.81, 217.572
A2, B2, C2 = 13.9320, 3056.96, 217.625
P = 120
X1 = 0.33
X2 = 1 - X1

expression = X1*sp.exp(A1 - B1/(t_var + C1)) + X2*sp.exp(A2 - B2/(t_var + C2)) - P
d_expression = sp.diff(expression, t_var)
derivative_0 = sp.lambdify(t_var, expression, "math")
derivative_1 = sp.lambdify(t_var, d_expression, "math")

T_INIT = 100 # degrees Celsius
t_prev = T_INIT
TOLERANCE = 1e-10
error = 100
num_iter = 0
MAX_ITER = 1000

while num_iter <= MAX_ITER and error > TOLERANCE:
    num_iter += 1
    print(f"Iteration #{num_iter}")
    t_next = t_prev - derivative_0(t_prev)/derivative_1(t_prev)
    error = abs(t_next - t_prev)
    print(f"error = {error}")
    print()

    if error <= TOLERANCE:
        print(f"T = {t_next}")
        break

    else:
        t_prev = t_next
