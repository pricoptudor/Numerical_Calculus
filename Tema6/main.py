import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


def function1(x):
    return x ** 2 - 12 * x + 30


def function2(x):
    return np.sin(x) - np.cos(x)


def function3(x):
    return 2 * (x ** 3) - 3 * x + 15


def square_func(x):
    return x * x


def generate_function_values(n, x_1, x_n, function):
    x = sorted([random.uniform(x_1, x_n) for _ in range(n-1)])
    x.insert(0, x_1)
    x.append(x_n)

    y = list(map(lambda k: function(k), x))

    return (x, y)

# --------------------------------------------------------------


def get_aitken_dif_div(x, f_x):
    y_current = [0 for _ in range(len(x))]
    y_previous = [0 for _ in range(len(x))]
    y_final = [0 for _ in range(len(x))]

    y_current[0] = f_x[0]
    y_final[0] = f_x[0]

    for i in range(1, len(x)):
        y_current[1] = (f_x[i] - f_x[i-1]) / (x[i] - x[i-1])

        for j in range(2, i+1):
            y_current[j] = (y_current[j-1] - y_previous[j-1]) / (x[i] - x[i-j])

        y_final[i] = y_current[i]
        y_previous = y_current.copy()

    return y_final


def calculate_newton_lagrange_solution(function, x, y, x_val):
    n = len(x)
    L = y[0]
    aikten = get_aitken_dif_div(x, y)
    for i in range(1, n):
        prod = 1
        for k in range(i):
            prod *= (x_val - x[k])
        L += aikten[i] * prod

    real_val = function(x_val)
    delta = abs(real_val - L)
    return L, real_val, delta

# --------------------------------------------------------------


def get_polynom_coefs(x, y, m):
    n = len(x)
    B = [[0 for _ in range(m)] for _ in range(m)]

    f = [0 for _ in range(m)]
    for i in range(m):
        sum = 0
        for k in range(n):
            sum += y[k] * (x[k] ** i)
        f[i] = sum

    for i in range(m):
        for j in range(m):
            sum = 0
            for k in range(n):
                sum += x[k] ** (i + j)
            B[i][j] = sum

    a = np.linalg.solve(B, f)
    return a


def get_polynom_val(a, m, x):
    d = a[m-1]
    for i in range(1, m):
        d = a[m-i-1] + d * x
    return d


def calculate_horner_sol(function, x, y, m, x_val):
    a = get_polynom_coefs(x, y, m)
    aprox_val = get_polynom_val(a, m, x_val)
    real_val = function(x_val)

    delta = abs(real_val - aprox_val)

    sum = 0
    for i in range(n):
        sum += abs(get_polynom_val(a, m, x[i]) - y[i])

    return aprox_val, real_val, delta, sum

# --------------------------------------------------------------


def bonus_newton_lagrange_solution(x, y, x_val):
    n = len(x)
    L = y[0]
    aikten = get_aitken_dif_div(x, y)
    for i in range(1, n):
        prod = 1
        for k in range(i):
            prod *= (x_val - x[k])
        L += aikten[i] * prod

    return L


def bonus_horner_sol(x, y, m, x_val):
    a = get_polynom_coefs(x, y, m)
    aprox_val = get_polynom_val(a, m, x_val)

    return aprox_val

# --------------------------------------------------------------


def draw_graphs(function, x_1, x_n, x, y, m):
    xx = np.linspace(x_1, x_n, 50)

    y1 = function(xx)
    y2 = bonus_newton_lagrange_solution(x, y, xx)
    y3 = bonus_horner_sol(x, y, m, xx)

    fig, axs = plt.subplots(1, 3, figsize=(14, 4))

    axs[0].plot(xx, y1)
    axs[1].plot(xx, y2)
    axs[2].plot(xx, y3)

    axs[0].set_title('Original Function')
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('y')
    axs[1].set_title('Newton Lagrange Estimation')
    axs[1].set_xlabel('x')
    axs[1].set_ylabel('y')
    axs[2].set_title('Square Horner Estimation')
    axs[2].set_xlabel('x')
    axs[2].set_ylabel('y')

    plt.show()

# --------------------------------------------------------------


n = 3
m = 5
x_1 = 0
x_n = 5


def solve_bonus():
    global n_entry
    global m_entry
    global x_1_entry
    global x_n_entry
    global x_val_entry
    global function_entry
    global response_text
    global content

    response_text.destroy()

    n = int(n_entry.get())
    m = int(m_entry.get())
    x_1 = float(x_1_entry.get())
    x_n = float(x_n_entry.get())
    x_val = float(x_val_entry.get())
    func_name = function_entry.get()

    if func_name == "func1":
        function = function1
    elif func_name == "func2":
        function = function2
    elif func_name == "func3":
        function = function3
    else:
        function = square_func

    x, y = generate_function_values(n, x_1, x_n, function)
    L, real1,  deltaL = calculate_newton_lagrange_solution(
        function, x, y, x_val)

    P, real2,  deltaP, sumP = calculate_horner_sol(function, x, y, m, x_val)

    response = f"L_n = {L} with delta = |L_n(x_val) - f(x_val)| = {deltaL}.\n"
    response += f"P_m = {P} with delta = |P_m(x_val) - f(x_val)| = {deltaP}.\n"
    response += f"|P_m(x_i) - y_i|, pentru i=(0..n), este: {sumP}"

    response_text = tk.Label(content,
                             padx=30,
                             text=response)
    response_text.grid(row=13)
    draw_graphs(function, x_1, x_n, x, y, m)


def bullet_homework():
    global content
    content.destroy()

    global n_entry
    global m_entry
    global x_1_entry
    global x_n_entry
    global x_val_entry
    global function_entry
    global response_text

    content = tk.Frame()
    content.pack(side='top')
    tk.Label(content,
             padx=30,
             text='n: ').grid(row=0)
    n_entry = tk.Entry(content,
                       width=50)
    n_entry.grid(row=1, padx=30)

    tk.Label(content,
             padx=30,
             text='m: ').grid(row=2)
    m_entry = tk.Entry(content,
                       width=50)
    m_entry.grid(row=3, padx=30)

    tk.Label(content,
             padx=30,
             text='x_1: ').grid(row=4)
    x_1_entry = tk.Entry(content,
                         width=50)
    x_1_entry.grid(row=5, padx=30)

    tk.Label(content,
             padx=30,
             text='x_n: ').grid(row=6)
    x_n_entry = tk.Entry(content,
                         width=50)
    x_n_entry.grid(row=7, padx=30)

    tk.Label(content,
             padx=30,
             text='x_val: ').grid(row=8)
    x_val_entry = tk.Entry(content,
                           width=50)
    x_val_entry.grid(row=9, padx=30)

    tk.Label(content,
             padx=30,
             text='function name: ').grid(row=10)
    function_entry = tk.Entry(content,
                              width=50)
    function_entry.grid(row=11, padx=30)

    tk.Button(content,
              text='SOLVE',
              padx=30,
              width=34,
              command=solve_bonus).grid(row=12)

    response_text = tk.Label(content,
                             padx=30,
                             text='')
    response_text.grid(row=13)


def gui():
    window = tk.Tk()
    global content
    window.geometry("800x600")
    window.configure(bg="cornsilk1")
    window.tk_setPalette(background='cornsilk1', foreground='black')

    buttons = tk.Frame()
    buttons.pack(side='top')
    button1 = tk.Button(buttons,
                        text='Homework',
                        width=20,
                        height=5,
                        command=bullet_homework)
    button1.grid(row=0, column=0)

    content = tk.Frame()

    window.mainloop()


gui()
