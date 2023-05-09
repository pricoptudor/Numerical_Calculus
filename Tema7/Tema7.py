import random 
import tkinter as tk
import numpy
import copy
from cmath import sqrt

# P(r) = a0 * r^n + a1 * r^(n-1) + ... + an

eps = 1e-6
kmax = 1000
poly = []
R = 0

def get_interval(poly):
    R = (abs(poly[0]) + max(map(abs, poly))) / abs(poly[0])
    return R

def horner(poly, x):
    n = len(poly)
    b = poly[0]
    for i in range(1, n):
        b_next = b * x + poly[i]
        b = b_next
    return b

def horner_complex(poly, x):
    n = len(poly)
    b_prev = None
    b = poly[0]
    if len(poly) == 1:
        return complex(b)
    c = x.real
    d = x.imag
    p = -2 * c
    q = c**2 + d**2
    b_prev = b
    b = poly[1] - p*b_prev
    for i in range(2, n):
        b_next = poly[i] - p*b - q*b_prev
        b_prev = b
        b = b_next
    return complex(b_prev*c+b+p*b_prev, b_prev*d)

print(horner_complex([1,-6,13,-12,4], 2))
# print(horner_complex([1, 1+2j, 2-3j, 4+5j, 3-4j], -1+2j))
# print(horner_complex([3+4j, 2-5j, 1+1j], 1-1j))

def derivative(poly):
    n = len(poly)
    if n == 1:
        return [0]
    else: 
        return [(n-i-1) * poly[i] for i in range(n-1)]
    
def sign(value):
    if value.real >= 0:
        return 1
    else: 
        return -1

def laguerre(poly):
    global R, kmax
    k = 0
    delta_x = 0
    # x = complex(random.uniform(-R, R), random.uniform(-R, R))
    x = complex(random.uniform(-R, R))

    while True:
        n = len(poly)
        first_der = derivative(poly)
        second_der = derivative(first_der)

        x_poly = horner_complex(poly, x)
        x_first_der = horner_complex(first_der, x)
        x_second_der = horner_complex(second_der, x)

        H = (n-1)**2 * x_first_der**2 - n*(n-1) * x_poly*x_second_der
        if H.real < 0 or abs(x_first_der + sign(x_first_der) * sqrt(H)) <= eps:
            print(f'Here: {H} ; {x} ; {x_poly} ; {x_first_der} ; {x_second_der}')
            print(f'delta: {abs(delta_x)}')
            break
        
        delta_x = (n * x_poly) / (x_first_der + sign(x_first_der) * sqrt(H))
        x -= delta_x
        k += 1

        if abs(delta_x) < eps or k > kmax or abs(delta_x) > 10**8:
            break
    
    if abs(delta_x) < eps:
        return x
    else: 
        return None

def find_solutions():
    global poly
    global R
    search = 60

    R = get_interval(poly)
    print(f'Poly: {poly}, R: {R}')
    polynom = copy.deepcopy(poly)
    solutions = [] 

    while len(polynom)>1 and search > 0:
        search -= 1
        sol = laguerre(polynom)
        print(f'Sol: {sol}')
        if sol is not None and sol not in solutions:
            solutions.append(sol)

            # divide polynom by (x-sol)
            polynom = numpy.polydiv(polynom, [1, -sol])[0]
    return solutions

def sol_to_file(solutions, path = 'solutions_7.txt'):
    global poly
    with open(path, 'a') as f:
        f.write(f'Polynom {poly} has solutions:\n')
        for sol in solutions:
            f.write(f'{sol}\n')

def bullet1_solve():
    global input_entry1
    global input_entry2
    global poly
    global kmax

    poly = eval(input_entry1.get())
    poly = [complex(i) for i in poly]
    kmax = eval(input_entry2.get())

    answer = 'Saved input:\n'
    answer += f'Poly coefficients: {poly}\n'
    answer += f'Max iterations: {kmax}\n'

    global content
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet1():
    global content
    content.destroy()

    global input_entry1
    global input_entry2

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text='Poly').grid(row=0)
    input_entry1 = tk.Entry(content,
             width=100)
    input_entry1.grid(row=1, padx=30)
    tk.Label(content,
                padx=30,
                text='Max iterations').grid(row=2)
    input_entry2 = tk.Entry(content,
             width=100)
    input_entry2.grid(row=3, padx=30)
    tk.Button(content,
              text='SAVE',
              padx=30,
              command=bullet1_solve).grid(row=8)

def bullet2():
    global content
    global poly
    global R
    content.destroy()

    R = get_interval(poly)
    answer = f'Poly roots are in interval: [-{R}, {R}]'
    
    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet3():
    global content, eps
    content.destroy()

    solutions = find_solutions()
    unique = []
    for i in range(len(solutions)):
        is_unique = True
        for j in range(i+1, len(solutions)):
            if abs(solutions[i] - solutions[j]) < eps:
                is_unique = False
                break
        if is_unique:
            unique.append(solutions[i])
    solutions = unique
    sol_to_file(solutions)
    solutions = set([complex(round(x.real, 3), round(x.imag, 3)) for x in solutions])
    answer = 'Roots are: ' + str(solutions)

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
                    text='[R, -R]',
                    width=20,
                    height=5,
                    command=bullet2)
button2.grid(row=0, column=1)

button3 = tk.Button(buttons,
                    text='Roots',
                    width=20,
                    height=5,
                    command=bullet3)
button3.grid(row=0, column=2)

content = tk.Frame()

window.mainloop()

# [1,-(3+1j),2+3j,0-2j] : 1, 2, i