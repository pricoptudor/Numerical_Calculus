import tkinter as tk
import numpy as np
import random
import copy
from math import sqrt

# Default values:
RANGE = 1000
m = 6
eps = 10 ** -m

n = 3

# [[60., 36., 143.], [80., 173., 149.], [-75., 5., 65.]]
A = np.array([[60., 36., 143.], 
              [80., 173., 149.], 
              [-75., 5., 65.]])
A_init = copy.deepcopy(A)
s = np.array(list(A[i][0] for i in range(n)))

# Ex. 1
def compute_b(A, s):
  n = len(A)  
  b = np.array([0.] * n)

  for i in range(n):
    b[i] = np.dot(s, A[i])

  # print(b)
  return b

b = compute_b(A, s)

# Ex. 2
def compute_QR(A):
  n = len(A)
  s = np.array(list(A[i][0] for i in range(n)))
  b = compute_b(A, s)

  Qt = np.eye(n)
  u = [0.] * n

  # print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A]))
  # print('Start Householder... \n')

  for r in range(n-1):
    sigma = 0 
    for i in range(r, n):
      sigma += A[i][r] * A[i][r]

    # print(f'sigma: {sigma}')

    if sigma <= eps:
      break

    k = sqrt(sigma)

    if A[r][r] > 0: 
      k = -k

    beta = sigma - k * A[r][r]

    u[r] = A[r][r] - k
    for i in range(r+1, n):
      u[i] = A[i][r]

    # print(f'u: {u}')
    # print(f'k: {k}')
    # print(f'beta: {beta}')

    for j in range(r+1, n):
      sum = 0 
      for i in range(r, n):
        sum += u[i] * A[i][j]
      omega = sum / beta

      for i in range(r, n):
        A[i][j] = A[i][j] - omega * u[i]
    
    A[r][r] = k
    for i in range(r+1, n):
      A[i][r] = 0
    
    sum = 0
    for i in range(r, n):
      sum += u[i] * b[i]
    omega = sum / beta

    for i in range(r, n):
      b[i] = b[i] - omega * u[i]

    for j in range(n):
      sum = 0
      for i in range(r, n):
        sum += u[i] * Qt[i][j]
      omega = sum / beta

      for i in range(r, n):
        Qt[i][j] = Qt[i][j] - omega * u[i]

    # print(f'step {r}')
    # print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A]))
    # print()
    # print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in Qt]))
    # print()

  return (np.array(Qt).T, np.array(A))

# Ex. 3
def compute_x_householder(A, b):
  Q, R = compute_QR(A)
  Qt = Q.T
  # print(f'Q:\n{Q}')
  # print(f'R:\n{R}')

  y = np.dot(Qt, b)
  x_householder = np.linalg.solve(R, y)
  # print(f'x_householder:\n{x_householder}')
  return x_householder

def compute_x_QR(A, b):
  Q, R = np.linalg.qr(A)
  # print(f'Q:\n{Q}')
  # print(f'R:\n{R}')
  Qt = Q.T

  y = np.dot(Qt, b)
  x_QR = np.linalg.solve(R, y)
  # print(f'x_QR:\n{x_QR}')
  return x_QR

def compute_norm_QR_householder(A, b):
  A = copy.deepcopy(A_init)
  x_householder = compute_x_householder(A, b)
  A = copy.deepcopy(A_init)
  x_QR = compute_x_QR(A, b)
  norm = np.linalg.norm(x_QR - x_householder)
  print(f"Norm is {norm}")
  return norm

# Ex. 4
def check1(A, b):
  A = copy.deepcopy(A_init)
  x_householder = compute_x_householder(A, b)
  norm = np.linalg.norm(np.matmul(A_init, x_householder) - b)
  print(f'Norm is: {norm}')
  return norm

def check2(A, b):
  A = copy.deepcopy(A_init)
  x_QR = compute_x_QR(A, b)
  norm = np.linalg.norm(np.matmul(A_init, x_QR) - b)
  print(f'Norm is: {norm}')
  return norm

def check3(A, b):
  A = copy.deepcopy(A_init)
  x_householder = compute_x_householder(A, b)
  norm = np.linalg.norm(x_householder - s) / np.linalg.norm(s)
  print(f'Norm is: {norm}')
  return norm

def check4(A, b):
  A = copy.deepcopy(A_init)
  x_QR = compute_x_QR(A, b)
  norm = np.linalg.norm(x_QR - s) / np.linalg.norm(s)
  print(f'Norm is: {norm}')
  return norm

# Ex. 5
def compute_householder_inv(A):
  A = copy.deepcopy(A_init)
  A_inv = np.array([[0.] * n for _ in range(n)])
  Q, R = compute_QR(A)

  if np.linalg.det(A) == 0:
    print('Cannot compute inverse!')
    return None

  for j in range(n):
    e = np.array([0] * n)
    e[j] = 1
    e = e.T

    b = np.matmul(Q.T, e)
    x = np.linalg.solve(R, b)
    
    A_inv[j] = x
    # print(f'A_inv: {A_inv}')

  A_inv = A_inv.T
  print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A_inv]))
  print()

  return A_inv

def compute_np_inv(A):
  A = copy.deepcopy(A_init)
  A_inv = np.linalg.inv(A)
  print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A_inv]))
  print()
  return A_inv

def compute_norm_inverse(A):
  A_inv_householder = compute_householder_inv(A)
  A_inv_np = compute_np_inv(A)

  norm = np.linalg.norm(A_inv_householder - A_inv_np)
  print(f'Norm is: {norm}')
  return norm

# Ex. 6
def random_init(n, numbers_range):
  global A_init
  A = np.array([[0.] * n for _ in range(n)])
  for i in range(n):
    for j in range(n):
      A[i][j] = random.random() * numbers_range
  A_init = copy.deepcopy(A)
  return A

# Bonus
def random_sym_init(n, numbers_range):
  global A_init
  A = np.array([[0.] * n for _ in range(n)])
  for i in range(n):
    for j in range(i+1):
      A[i][j] = random.random() * numbers_range
      A[j][i] = A[i][j]
  A_init = copy.deepcopy(A)
  return A

def mul_RQ(R, Q):
  dim = len(R)
  A = np.array([[0.] * dim for _ in range(dim)])
  for i in range(dim):
    for j in range(dim):
      for k in range(i, dim):
        A[i][j] += R[i][k] * Q[k][j]
  return A

def lim_householder(A):
  A, R = compute_QR(A)
  if np.linalg.norm(mul_RQ(R, A) - np.matmul(A, R)) <= eps:
    return mul_RQ(R, A)
  
  A = mul_RQ(R, A)
  return lim_householder(A)




def bullet1_solve():
    global input_entry1
    global input_entry2
    global input_entry3
    global m
    global eps
    global A
    global A_init
    global n
    global b
    global s

    m = eval(input_entry1.get())
    eps = 10 ** -m
    n = eval(input_entry2.get())
    matrix = input_entry3.get()
    if matrix == 'sym':
      A = random_sym_init(n, numbers_range=RANGE)
    elif matrix == 'random':
      A = random_init(n, numbers_range=RANGE)
    else:
      A = eval(matrix)
    A_init = copy.deepcopy(A)
    s = np.array(list(A[i][0] for i in range(n)))
    b = compute_b(A, s)

    print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A_init]))

    answer = 'Saved input:\n'
    answer += f'eps: {eps}\n'
    answer += f'n: {n}\n'
    answer += f'b: {str(b)}\n'
    answer += f's: {str(s)}\n'
    answer += 'A: \n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A])

    global content
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet1():
    global content
    content.destroy()

    global input_entry1
    global input_entry2
    global input_entry3

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text='m for epsilon <- 10^-m').grid(row=0)
    input_entry1 = tk.Entry(content,
             width=100)
    input_entry1.grid(row=1, padx=30)
    tk.Label(content,
                padx=30,
                text='n for matrix A : nxn').grid(row=2)
    input_entry2 = tk.Entry(content,
             width=100)
    input_entry2.grid(row=3, padx=30)
    tk.Label(content,
                padx=30,
                text='matrix A or "sym"/"random"').grid(row=4)
    input_entry3 = tk.Entry(content,
             width=100)
    input_entry3.grid(row=5, padx=30)
    tk.Button(content,
              text='SAVE',
              padx=30,
              command=bullet1_solve).grid(row=8)

def bullet2():
    global content
    content.destroy()

    global A_init

    A = copy.deepcopy(A_init)
    Q, R  = compute_QR(A)

    answer = 'Q:\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in Q])
    answer += '\nR\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in R])

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet3():
    global content
    content.destroy()

    global A_init
    global b

    A = copy.deepcopy(A_init)
    norm = compute_norm_QR_householder(A, b)

    answer = f'The norm of solutions is {norm}'

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet4():
    global content
    content.destroy()

    global A_init

    error1 = check1(copy.deepcopy(A_init), b)
    error2 = check2(copy.deepcopy(A_init), b)
    error3 = check3(copy.deepcopy(A_init), b)
    error4 = check4(copy.deepcopy(A_init), b)

    answer = f'The first error is {error1}\n'
    answer += f'The second error is {error2}\n'
    answer += f'The third error is {error3}\n'
    answer += f'The fourth error is {error4}\n'

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)

def bullet5():
    global content
    content.destroy()

    global A_init
    A = copy.deepcopy(A_init)
    
    norm = compute_norm_inverse(A)

    answer = f'Norm of inverse: {norm}'

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=9)
    
def bullet6():
    global content
    content.destroy()

    global s
    global b
    global A

    A = random_sym_init(n, RANGE)
    s = np.array(list(A[i][0] for i in range(n)))
    b = compute_b(A, s)

    A_lim = lim_householder(A)
    
    answer = 'The limit of the Householder series:\n'
    answer += '\n'.join(['  |  '.join([str(cell) for cell in row]) for row in A_lim])

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
                    text='QR Householder',
                    width=20,
                    height=5,
                    command=bullet2)
button2.grid(row=0, column=1)

button3 = tk.Button(buttons,
                    text='x_QR/Hh norm',
                    width=20,
                    height=5,
                    command=bullet3)
button3.grid(row=0, column=2)

button4 = tk.Button(buttons,
                    text='Errors',
                    width=20,
                    height=5,
                    command=bullet4)
button4.grid(row=0, column=3)

button5 = tk.Button(buttons,
                    text='Inverse norm',
                    width=20,
                    height=5,
                    command=bullet5)
button5.grid(row=0, column=4)

button6 = tk.Button(buttons,
                    text='Check limit',
                    width=20,
                    height=5,
                    command=bullet6)
button6.grid(row=0, column=5)

content = tk.Frame()

window.mainloop()