import sympy as sp

P = 100

def k_value(specie: int) -> float:
    if specie == 1:
        P1SAT = 195.75
        K = P1SAT/P
    elif specie == 2:
        P1SAT = 97.84
        K = P1SAT/P
    elif specie == 3:
        P1SAT = 50.32
        K = P1SAT/P
    return K

Vfrac_var = sp.symbols("Vfrac_var")

def xi_expr(specie: int):
    if specie == 1:
        Z = 0.45
        x = Z/(1 + Vfrac_var*(k_value(1)-1))
    elif specie == 2:
        Z = 0.35
        x = Z/(1 + Vfrac_var*(k_value(2)-1))
    elif specie == 3:
        Z = 0.20
        x = Z/(1 + Vfrac_var*(k_value(3)-1))
    return x

main_expr = xi_expr(1) + xi_expr(2) + xi_expr(3) - 1
diff_main_expr = sp.diff(main_expr, Vfrac_var)
main_formula = sp.lambdify(Vfrac_var, main_expr)
diff_formula = sp.lambdify(Vfrac_var, diff_main_expr)

vfrac_old = 0
no_error = False
num_iter = 1
max_iter = 1000
TOLERANCE = 1e-6
while num_iter <= max_iter:
    while not no_error:
        print("iteration #", num_iter)
        vfrac_new = vfrac_old - main_formula(vfrac_old)/diff_formula(vfrac_old)
        error = abs(vfrac_new - vfrac_old)
        if error < TOLERANCE:
            print("V/F =", vfrac_new)
            break
        else:
            num_iter += 1
            vfrac_new = vfrac_old
            print("error =",error)
            print()

