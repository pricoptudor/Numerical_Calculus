import math
import random
import tkinter as tk

func = None
kmax = 1000
epsilon = 10 ** (-4)
rand_range = 10

def f1(x):
    return 1.0 / 3.0 * (x ** 3) - 2 * (x ** 2) + 2 * x + 3

def f2(x):
    return x ** 2 + math.sin(x)

def f3(x):
    return (x ** 4) - 6 * (x ** 3) + 13 * (x ** 2) - 12 * x + 4

def derivative_g1_x(f, x, h=10 ** (-6)):
    return (3 * f(x) - 4 * f(x - h) + f(x - 2 * h)) / (2 * h)

def derivative_g2_x(f, x, h=10 ** (-6)):
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)

def second_derivative_x(f, x, h=10 ** (-6)):
    return (-f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x - h) - f(x - 2 * h)) / (12 * h * h)

def solve_secanta(f, x, x_prev, deriv):
    k = 0
    while True:
        g_x = deriv(f, x)
        g_x_prev = deriv(f, x_prev)
        delta_x = ((x-x_prev) * g_x) / (g_x - g_x_prev) 
        if abs(g_x - g_x_prev) <= epsilon:
            if abs(g_x) <= epsilon/100:
                if second_derivative_x(f, x) > 0:
                    delta_x = 0
                    return x, k
            else:
                delta_x = 10**-5
        x_prev = x
        x = x - delta_x
        k += 1
        if abs(delta_x) < epsilon or k >= kmax or abs(delta_x) >= 10**8:
            break
    if abs(delta_x) < epsilon:
        if second_derivative_x(f, x) > 0:
            return x, k
    else:
        return None
    
def exists_sol(solutions, x):
    # print(f'Solutions: {solutions}')
    for sol in solutions:
        if abs(sol - x) < epsilon:
            return True
    return False

def compute_solutions(f, deriv):
    solutions = []
    iterations = []
    for i in range(100):
        x = random.uniform(-rand_range, rand_range)
        x_prev = random.uniform(-rand_range, rand_range)
        solution = solve_secanta(f, x, x_prev, deriv)
        if solution is not None:
            solution, iteration = solution
            if not exists_sol(solutions, solution):
                solutions.append(solution)
                iterations.append(iteration)
    return solutions, iterations

def sol_to_file(solutions_g1, solutions_g2, path = 'solutions_8.txt'):
    with open(path, 'w') as f:
        f.write(f'G1: {solutions_g1} \n')
        f.write(f'G2: {solutions_g2}')

print(compute_solutions(f1, derivative_g1_x))
print(compute_solutions(f2, derivative_g1_x))
print(compute_solutions(f3, derivative_g1_x))
print(compute_solutions(f1, derivative_g2_x))
print(compute_solutions(f2, derivative_g2_x))
print(compute_solutions(f3, derivative_g2_x))

def bullet1_solve():
    global input_entry
    global func

    func_x = input_entry.get()
    def fx(x):
        return eval(func_x)
    func = fx

    answer = 'Saved input!'

    global content
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet1():
    global content
    content.destroy()

    global input_entry
    
    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text='Function').grid(row=0)
    input_entry = tk.Entry(content,
             width=100)
    input_entry.grid(row=1, padx=30)
    tk.Button(content,
              text='SAVE',
              padx=30,
              command=bullet1_solve).grid(row=8)

def bullet2():
    global content
    global func
    content.destroy()

    g1_sol = compute_solutions(func, derivative_g1_x)
    g2_sol = compute_solutions(func, derivative_g2_x)
    sol_to_file(g1_sol, g2_sol)

    answer = 'Solutions-iterations computed with g1_derivative:\n'
    answer += str(g1_sol)
    answer += '\n\n'
    answer += 'Solutions-iterations computed with g2_derivative:\n'
    answer += str(g2_sol)

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)


# GUI:
window = tk.Tk()
window.geometry("1000x800")

buttons = tk.Frame()
buttons.pack(side='top')
button1 = tk.Button(buttons,
                    text='Input',
                    width=20,
                    height=5,
                    command=bullet1)
button1.grid(row=0, column=0)

button2 = tk.Button(buttons,
                    text='Compare solutions',
                    width=20,
                    height=5,
                    command=bullet2)
button2.grid(row=0, column=1)

content = tk.Frame()

window.mainloop()