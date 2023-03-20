import tkinter as tk
import numpy as np
import random
import copy

m = 6
eps = 10 ** -m

n = 3

A = [[1, 2.5, 3], [2.5, 8.25, 15.5], [3, 15.5, 43]]
A_init = copy.deepcopy(A)

D = []

b = [12, 38, 68]

# test division:
def test_div(v):
  if abs(v) > eps:
    return True
  else:
    print('Cannot divide by ~0')
    return False

def cholesky(A):
  D = [0] * n

  for p in range(n):
    # compute d_p
    prev_sum = 0
    for k in range(p):
      prev_sum += D[k] * A[p][k] * A[p][k]
    D[p] = A[p][p] - prev_sum

    if not test_div(D[p]):
      print("Choleski cannot be computed")
      return

    # compute l_ip
    for i in range(p+1, n):
      prev_sum = 0
      for k in range(p):
        prev_sum += D[k] * A[i][k] * A[p][k]
      A[i][p] = (A[p][i] - prev_sum) / D[p]

  return (A, D)

A, D = cholesky(A)

# det L == det L^T == 1 (matrice triunghiulara => produs pe diagonala)
# => det A == det D == produs pe diagonala
def determinant(A):
  A, D = cholesky(A)
  det = 1
  for i in range(n):
    det *= D[i]
  return det

# solve L * z == b
def step_1(A, b):
  z = [0] * n
  for i in range(n):
    sum = 0
    for j in range(i):
      sum += A[i][j] * z[j]
    z[i] = b[i] - sum
  return z

# solve D * y == z
def step_2(D, z):
  y = [0] * n
  for i in range(n):
    y[i] = z[i] / D[i]
  return y

# solve L^T * x == y
def step_3(A, y):
  x = [0] * n
  for i in range(n-1, -1, -1):
    sum = 0
    for j in range(i+1, n):
      sum += A[j][i] * x[j]
    x[i] = y[i] - sum
  return x

# solve A * x = b
def solve(A, b):
  A, D = cholesky(A)
  z = step_1(A, b)
  print('z:\n', z)
  y = step_2(D, z)
  print('y:\n', y)
  x = step_3(A, y)
  print('x:\n', x)
  return x

xchol = solve(A, b)

# A factorization into L*U
L = np.linalg.cholesky(A)
U = L.T.conj()
print(L,'\n\n', U, '\n\n')
np.dot(L, U)

# solution to A * x = b
x = np.linalg.solve(A, b)

# Computed like this is approximated to 0, should I do it manually?
distance = np.linalg.norm(np.dot(A_init, xchol) - b)
if distance < eps:
  print('Solution is good')
else:
  print('Recompute solution for Cholesky')

def matrix_sym(n):
  matrix = [[0 for j in range(n)] for i in range(n)]

  # populate the matrix with values
  for i in range(n):
      for j in range(i+1):
          matrix[i][j] = random.random() * 100
          matrix[j][i] = matrix[i][j]
  return matrix

def matrix_sym_pos(n):
  matrix = matrix_sym(n)

  for i in range(n):
    matrix[i][i] = random.randint(1, 100) * 100 * n
  
  return matrix


# L * D => matrice nx1; inmultim numerele din liniile din A cu elementele din D,
#              pana in diagonala principala inclusiv, considerand ca aceasta e 1 
def check_cholesky(A, D, A_init):
  # L * D
  for i in range(n):
    for j in range(i+1):
      if i == j:
        A[i][j] = D[j]
      else:
        A[j][i] = A[i][j] * D[j]

  # C:
  # 1    2.5  3
  # 2.5  2    8
  # 3    4    2

  # C00 <- C00 * 1
  # C01 <- C00 * C10
  # C02 <- C00 * C20

  # C10 <- C01 * 1
  # C11 <- C01 * C10 + C11 * 1
  # C12 <- C01 * C20 + C11 * C21

  # C20 <- C02 * 1
  # C21 <- C02 * C10 + C12 * 1
  # C22 <- C02 * C20 + C12 * C21 + C22 * 1

  # (L*D) * L^T
  print('n:',n)
  for i in range(n):
    for j in range(n):
      sum = 0
      for k in range(min(i,j) + 1):
        sum += A[k][i] * (A[j][k] if j!=k else 1)
        
      print(sum, ';', A_init[i][j])
      if abs(sum - A_init[i][j]) > eps:
        return 'Matrices not equal'

  return 'Equal matrices'


def bullet1_solve():
    global input_entry1
    global input_entry2
    global input_entry3
    global input_entry4
    global m
    global eps
    global A
    global A_init
    global n
    global b

    m = eval(input_entry1.get())
    eps = 10 ** -m
    n = eval(input_entry2.get())
    b = eval(input_entry4.get())
    matrix = input_entry3.get()
    if matrix == 'sym':
      A = matrix_sym(n)
    elif matrix == 'sym_pos':
      A = matrix_sym_pos(n)
    else:
      A = eval(matrix)
    A_init = copy.deepcopy(A)

    print('\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in A_init]))

    answer = 'Saved input:\n'
    answer += f'eps: {eps}\n'
    answer += f'n: {n}\n'
    answer += f'b: {str(b)}\n'
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
    global input_entry4

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
                text='matrix A or "sym"/"sym_pos"').grid(row=4)
    input_entry3 = tk.Entry(content,
             width=100)
    input_entry3.grid(row=5, padx=30)
    tk.Label(content,
                padx=30,
                text='b for Ax=b').grid(row=6)
    input_entry4 = tk.Entry(content,
             width=100)
    input_entry4.grid(row=7, padx=30)
    tk.Button(content,
              text='SAVE',
              padx=30,
              command=bullet1_solve).grid(row=8)

def bullet2():
    global content
    content.destroy()

    global A
    global D
    global n
    A, D = cholesky(A)

    L_matrix = [[0] * n for _ in range(n)]
    D_matrix = [[0] * n for _ in range(n)]
    LT_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
      D_matrix[i][i] = D[i]
      L_matrix[i][i] = 1
      LT_matrix[i][i] = 1
      for j in range(i):
        L_matrix[i][j] = A[i][j]
        LT_matrix[j][i] = A[i][j]

    answer = 'L:\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in L_matrix])
    answer += '\nD:\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in D_matrix])
    answer += '\nLT:\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in LT_matrix])

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=0)

def bullet3():
    global content
    content.destroy()

    global A
    global A_init

    A = copy.deepcopy(A_init)
    det = determinant(A)

    answer = f'Determinant of A: {det}'

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=0)

def bullet4():
    global content
    content.destroy()

    global A
    global A_init
    global b

    A = copy.deepcopy(A_init)
    xchol = solve(A, b)

    answer = f'Solution of A * x == b: {str(xchol)}'

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=0)

def bullet5():
    global content
    content.destroy()

    global A
    global A_init
    global b

    A = copy.deepcopy(A_init)
    
    L = np.linalg.cholesky(A)
    U = L.T.conj()

    x = np.linalg.solve(A, b)

    answer = 'L:\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in L])
    answer += '\nU:\n'
    answer += '\n'.join([' '.join(['{:14f}'.format(cell) for cell in row]) for row in U])
    answer += '\nx:\n'
    answer += str(x)

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=0)

def bullet6():
    global content
    content.destroy()

    global A_init
    global b

    A = copy.deepcopy(A_init)
    xchol = solve(A, b)
    distance = np.linalg.norm(np.dot(A_init, xchol) - b)

    if distance < eps:
        answer = 'Solution is good'
    else:
        answer = 'Recompute solution for Cholesky'

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=0)

def bulletbonus():
    global content
    content.destroy()

    global A
    global A_init
    global D

    A = copy.deepcopy(A_init)
    A, D = cholesky(A)

    answer = check_cholesky(A, D, A_init)

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
                padx=30,
                text=answer).grid(row=0)


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
                    text='Cholesky factorization',
                    width=20,
                    height=5,
                    command=bullet2)
button2.grid(row=0, column=1)

button3 = tk.Button(buttons,
                    text='Determinant',
                    width=20,
                    height=5,
                    command=bullet3)
button3.grid(row=0, column=2)

button4 = tk.Button(buttons,
                    text='x_Chol',
                    width=20,
                    height=5,
                    command=bullet4)
button4.grid(row=0, column=3)

button5 = tk.Button(buttons,
                    text='Numpy Cholesky',
                    width=20,
                    height=5,
                    command=bullet5)
button5.grid(row=0, column=4)

button6 = tk.Button(buttons,
                    text='Check norm',
                    width=20,
                    height=5,
                    command=bullet6)
button6.grid(row=0, column=4)

button7 = tk.Button(buttons,
                    text='Check Cholesky',
                    width=20,
                    height=5,
                    command=bulletbonus)
button7.grid(row=0, column=5)

content = tk.Frame()

window.mainloop()