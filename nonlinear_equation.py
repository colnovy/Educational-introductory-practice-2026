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
