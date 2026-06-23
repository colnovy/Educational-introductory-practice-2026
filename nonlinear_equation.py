import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

x = sp.Symbol('x')

func_str = input("Введите функцию f(x): ")

try:
    expr = sp.sympify(func_str)
except sp.SympifyError:
    print("Ошибка в записи функции!")
    exit()

f = sp.lambdify(x, expr, 'numpy')

x_vals = np.linspace(-10, 10, 400)
y_vals = f(x_vals)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, label=f"f(x) = {func_str}", color='royalblue')
plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.title("График функции для поиска корней")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.show()


print("\n\nМЕТОД БИСЕКЦИИ")
def bisection_method(f, a, b, eps, max_iter=100):

    results = []

    if f(a) * f(b) >= 0:
        print("Ошибка: функция не меняет знак на отрезке [a, b]")
        return None

    iteration = 0
    while iteration < max_iter:
        c = (a + b) / 2
        fc = f(c)

        results.append({
            'Итерация': iteration + 1,
            'a': a,
            'b': b,
            'c (середина)': c,
            'f(c) (невязка)': fc
        })

        if abs(fc) < eps:
            return results

        if f(a) * fc < 0:
            b = c
        else:
            a = c

        iteration += 1

    print(f"Достигнуто максимальное число итераций ({max_iter})")
    return results

a = float(input("Введите левую границу отрезка a: "))
b = float(input("Введите правую границу отрезка b: "))
eps = float(input("Введите точность eps (например, 0.0001): "))

bisection_results = bisection_method(f, a, b, eps)

if bisection_results:
    df_bisection = pd.DataFrame(bisection_results)
    print("\nТаблица итераций метода бисекции:")
    print(df_bisection.to_string(index=False))

print("\n\nМЕТОД НЬЮТОНА (КАСАТЕЛЬНЫХ)")
df_expr = sp.diff(expr, x)
df = sp.lambdify(x, df_expr, 'numpy')

print(f"\nПроизводная функции: f'(x) = {df_expr}")

def newton_method(f, df, x0, eps, max_iter=100):

    results = []
    x_n = x0
    iteration = 0

    while iteration < max_iter:
        fx = f(x_n)
        dfx = df(x_n)

        results.append({
            'Итерация': iteration + 1,
            'x_n': x_n,
            'f(x_n) (невязка)': fx,
            "f'(x_n)": dfx
        })

        if abs(fx) < eps:
            return results

        if abs(dfx) < 1e-10:
            print("Ошибка: производная равна нулю, метод неприменим")
            return None

        x_next = x_n - fx / dfx
        x_n = x_next
        iteration += 1

    print(f"Достигнуто максимальное число итераций ({max_iter})")
    return results

x0 = float(input("Введите начальное приближение x0: "))

newton_results = newton_method(f, df, x0, eps)

if newton_results:
    df_newton = pd.DataFrame(newton_results)
    print("\nТаблица итераций метода Ньютона:")
    print(df_newton.to_string(index=False))

print("\n\nМЕТОД СЕКУЩЕЙ")
def secant_method(f, x0, x1, eps, max_iter=100):

    results = []
    iteration = 0

    while iteration < max_iter:
        fx0 = f(x0)
        fx1 = f(x1)

        results.append({
            'Итерация': iteration + 1,
            'x_{n-1}': x0,
            'x_n': x1,
            'f(x_n) (невязка)': fx1
        })

        if abs(fx1) < eps:
            return results

        if abs(fx1 - fx0) < 1e-10:
            print("Ошибка: деление на ноль, метод неприменим")
            return None

        x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

        x0 = x1
        x1 = x_next
        iteration += 1

    print(f"Достигнуто максимальное число итераций ({max_iter})")
    return results

x0_sec = float(input("Введите первое начальное приближение x0: "))
x1_sec = float(input("Введите второе начальное приближение x1: "))

secant_results = secant_method(f, x0_sec, x1_sec, eps)

if secant_results:
    df_secant = pd.DataFrame(secant_results)
    print("\nТаблица итераций метода секущих:")
    print(df_secant.to_string(index=False))
