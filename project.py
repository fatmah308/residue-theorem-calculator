import sympy as sp
from sympy import symbols, I, pi, simplify, re, im

class ResidueCalculator:
    def __init__(self):
        self.z = symbols('z')

    def get_function(self):
        while True:
            try:
                expr = input("Enter f(z) (e.g., '1/(z**2+1)', 'exp(z)/z**3'): ").replace('^','**')
                return sp.sympify(expr)
            except:
                print("Invalid input. Try again.")

    def get_contour(self):
        print("\nContour options:")
        print("1. Circle |z| = R")
        print("2. Rectangle")
        choice = input("Choose contour (1-2): ").strip()
        
        if choice == '1':
            R = float(input("Enter radius R: "))
            return ('circle', R)
        else:
            xmin = float(input("x_min: "))
            xmax = float(input("x_max: "))
            ymin = float(input("y_min: "))
            ymax = float(input("y_max: "))
            return ('rectangle', (xmin, xmax, ymin, ymax))

    def find_poles(self, f):
        denom = f.as_numer_denom()[1]
        roots = sp.roots(denom, self.z)
        return [(r, m) for r, m in roots.items() if not sp.simplify(f.subs(self.z, r)).is_zero]

    def calculate_residue(self, f, pole, order):
        if order == 1:
            return simplify((self.z - pole)*f).subs(self.z, pole)
        else:
            expr = (self.z - pole)**order * f
            deriv = expr.diff(self.z, order-1)
            return simplify(deriv.subs(self.z, pole) / sp.factorial(order-1))

    def is_inside(self, point, contour):
        if contour[0] == 'circle':
            return abs(point) < contour[1]
        else:
            x, y = re(point), im(point)
            bounds = contour[1]
            return bounds[0] < x < bounds[1] and bounds[2] < y < bounds[3]

    def compute(self):
        print("\n=== Residue Theorem Calculator ===")
        f = self.get_function()
        contour = self.get_contour()
        
        poles = self.find_poles(f)
        inside_poles = [(p, m) for p, m in poles if self.is_inside(p, contour)]
        
        if not inside_poles:
            print("\nResult: 0 (no poles inside contour)")
            return

        total = 0
        print("\nPoles inside contour:")
        for p, m in inside_poles:
            res = self.calculate_residue(f, p, m)
            print(f"• {p}: residue = {res}")
            total += res

        result = 2*pi*I*total
        print("\nFinal Result:")
        print(f"2πi × (Sum of residues) = {simplify(result)}")
        print(f"Numerical value: {result.evalf()}")

if __name__ == "__main__":
    ResidueCalculator().compute()
