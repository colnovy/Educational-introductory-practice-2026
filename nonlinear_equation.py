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
