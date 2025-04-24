from typing import Tuple
from sympy import symbols, lambdify
import math

A, B, C, T = symbols("A, B, C, T")
Antoine_P_expr = math.e**(A - B / (T + C))
Antoine_P = lambdify((A, B, C, T), Antoine_P_expr) 

def m_BUBL_P(x1, Temp_C, A1, B1, C1, A2, B2, C2) -> Tuple[float, float]:
    """
    Return (y1, P)
    """

    P1_sat = Antoine_P(A1, B1, C1, Temp_C)
    P2_sat = Antoine_P(A2, B2, C2, Temp_C)

    x2 = 1 - x1
    const = 2.771 - 0.00523*(Temp_C+273.15)
    gamma1 = math.e**(const*(x2)**2)
    gamma2 = math.e**(const*(x1)**2)
    print(gamma1, gamma2)

    P = x1*gamma1*P1_sat + x2*gamma2*P2_sat

    y1 = x1*gamma1*P1_sat/P

    return (y1, P)

y1, P = m_BUBL_P(0.25, 45, 16.5785, 3638.27, 239.500, 14.2456, 2662.78, 219.690)
print("(a)")
print("y1 =",y1) 
print("y2 =",1-y1)
print("P =",P) 
print()

