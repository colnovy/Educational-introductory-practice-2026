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

def plot_bisection(f, results, ax):

    a_init = results[0]['a']
    b_init = results[0]['b']
    x_min = a_init - 0.5
    x_max = b_init + 0.5
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = f(x_vals)

    ax.plot(x_vals, y_vals, 'darkgray', linewidth=2, label='f(x)')
    ax.axhline(0, color='black', linewidth=1)

    colors = plt.cm.coolwarm(np.linspace(0, 1, len(results)))

    for i, res in enumerate(results):
        a, b, c = res['a'], res['b'], res['c (середина)']
        fc = res['f(c) (невязка)']

        ax.axvspan(a, b, alpha=0.1, color=colors[i])

        ax.plot(c, fc, 'ro', markersize=6)
        ax.plot(c, 0, 'rv', markersize=8)
        ax.annotate(f'c{i + 1}', (c, 0), textcoords="offset points",
                    xytext=(0, -15), ha='center', fontsize=8)

    ax.set_title('Метод бисекции')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_newton(f, df, results, ax):

    x_points = [res['x_n'] for res in results]
    x_min = min(x_points) - 1
    x_max = max(x_points) + 1
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = f(x_vals)

    ax.plot(x_vals, y_vals, 'darkgray', linewidth=2, label='f(x)')
    ax.axhline(0, color='black', linewidth=1)

    colors = plt.cm.autumn(np.linspace(0, 1, len(results)))

    for i, res in enumerate(results):
        x_n = res['x_n']
        fx = res['f(x_n) (невязка)']
        dfx = res["f'(x_n)"]

        ax.plot(x_n, fx, 'o', color=colors[i], markersize=8)

        if i < len(results) - 1:
            x_next = results[i + 1]['x_n']
        else:
            x_next = x_n - fx / dfx if abs(dfx) > 1e-10 else x_n

        x_tangent = np.linspace(x_n, x_next, 50)
        y_tangent = fx + dfx * (x_tangent - x_n)
        ax.plot(x_tangent, y_tangent, '--', color=colors[i], linewidth=1.5, alpha=0.7)

        ax.plot(x_next, 0, 'v', color=colors[i], markersize=8)
        ax.annotate(f'x{i + 1}', (x_next, 0), textcoords="offset points",
                    xytext=(0, -15), ha='center', fontsize=8, color=colors[i])

    ax.set_title('Метод Ньютона')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_secant(f, results, ax):

    x_points = [res['x_n'] for res in results]
    x_prev = results[0]['x_{n-1}']
    all_x = [x_prev] + x_points
    x_min = min(all_x) - 1
    x_max = max(all_x) + 1
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = f(x_vals)

    ax.plot(x_vals, y_vals, 'darkgray', linewidth=2, label='f(x)')
    ax.axhline(0, color='black', linewidth=1)

    colors = plt.cm.viridis(np.linspace(0, 1, len(results)))

    for i, res in enumerate(results):
        x_prev_i = res['x_{n-1}']
        x_n = res['x_n']
        fx_prev = f(x_prev_i)
        fx_n = res['f(x_n) (невязка)']

        ax.plot(x_prev_i, fx_prev, 'o', color=colors[i], markersize=6, alpha=0.6)
        ax.plot(x_n, fx_n, 'o', color=colors[i], markersize=8)

        if i < len(results) - 1:
            x_next = results[i + 1]['x_n']
        else:

            if abs(fx_n - fx_prev) > 1e-10:
                x_next = x_n - fx_n * (x_n - x_prev_i) / (fx_n - fx_prev)
            else:
                x_next = x_n

        x_secant = np.linspace(x_prev_i, x_next, 50)

        if abs(x_n - x_prev_i) > 1e-10:
            slope = (fx_n - fx_prev) / (x_n - x_prev_i)
            y_secant = fx_prev + slope * (x_secant - x_prev_i)
            ax.plot(x_secant, y_secant, '--', color=colors[i], linewidth=1.5, alpha=0.7)

        ax.plot(x_next, 0, 'v', color=colors[i], markersize=8)
        ax.annotate(f'x{i + 1}', (x_next, 0), textcoords="offset points",
                    xytext=(0, -15), ha='center', fontsize=8, color=colors[i])

    ax.set_title('Метод секущих')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    ax.grid(True, alpha=0.3)

if bisection_results and newton_results and secant_results:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    plot_bisection(f, bisection_results, axes[0])
    plot_newton(f, df, newton_results, axes[1])
    plot_secant(f, secant_results, axes[2])

    plt.tight_layout()
    plt.show()
else:
    print("Графики не могут быть построены, так как не все методы отработали успешно.")

import time

def measure_time(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return result, end - start

bis_res, bis_time = measure_time(bisection_method, f, a, b, eps)
new_res, new_time = measure_time(newton_method, f, df, x0, eps)
sec_res, sec_time = measure_time(secant_method, f, x0_sec, x1_sec, eps)

comparison_data = {
    'Метод': ['Бисекция', 'Ньютона', 'Секущих'],
    'Количество итераций': [
        len(bis_res) if bis_res else 'Ошибка',
        len(new_res) if new_res else 'Ошибка',
        len(sec_res) if sec_res else 'Ошибка'
    ],
    'Время выполнения (мс)': [
        f"{bis_time * 1000:.4f}" if bis_res else 'Ошибка',
        f"{new_time * 1000:.4f}" if new_res else 'Ошибка',
        f"{sec_time * 1000:.4f}" if sec_res else 'Ошибка'
    ],
    'Найденный корень': [
        f"{bis_res[-1]['c (середина)']:.6f}" if bis_res else 'Ошибка',
        f"{new_res[-1]['x_n']:.6f}" if new_res else 'Ошибка',
        f"{sec_res[-1]['x_n']:.6f}" if sec_res else 'Ошибка'
    ],
    'Финальная невязка |f(x)|': [
        f"{abs(bis_res[-1]['f(c) (невязка)']):.2e}" if bis_res else 'Ошибка',
        f"{abs(new_res[-1]['f(x_n) (невязка)']):.2e}" if new_res else 'Ошибка',
        f"{abs(sec_res[-1]['f(x_n) (невязка)']):.2e}" if sec_res else 'Ошибка'
    ]
}

df_comparison = pd.DataFrame(comparison_data)
print("\nТаблица сравнения:")
print(df_comparison.to_string(index=False))

if bis_res and new_res and sec_res:
    fig, ax = plt.subplots(figsize=(10, 6))

    bis_errors = [abs(res['f(c) (невязка)']) for res in bis_res]
    new_errors = [abs(res['f(x_n) (невязка)']) for res in new_res]
    sec_errors = [abs(res['f(x_n) (невязка)']) for res in sec_res]

    bis_iters = list(range(1, len(bis_errors) + 1))
    new_iters = list(range(1, len(new_errors) + 1))
    sec_iters = list(range(1, len(sec_errors) + 1))

    ax.semilogy(bis_iters, bis_errors, 'o-', linewidth=2, markersize=6,
                label=f'Бисекция ({len(bis_errors)} ит.)', color='royalblue')
    ax.semilogy(new_iters, new_errors, 's-', linewidth=2, markersize=6,
                label=f'Ньютона ({len(new_errors)} ит.)', color='red')
    ax.semilogy(sec_iters, sec_errors, '^-', linewidth=2, markersize=6,
                label=f'Секущих ({len(sec_errors)} ит.)', color='purple')

    ax.axhline(eps, color='black', linestyle='--', linewidth=1,
               label=f'Точность ε = {eps}')

    ax.set_xlabel('Номер итерации', fontsize=12)
    ax.set_ylabel('Невязка |f(x)| (лог. шкала)', fontsize=12)
    ax.set_title('Сравнение скорости сходимости методов', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.show()
else:
    print("Не все методы отработали успешно, график сходимости не может быть построен.")
