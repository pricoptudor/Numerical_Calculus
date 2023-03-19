import tkinter as tk
import random
import numpy as np

def ex1_sol():
    m = 1
    u = 0.1
    while 1 + u != 1:
        m += 1
        u /= 10
    u *= 10

    return u

def ex1():
    global content
    content.destroy()

    sol = ex1_sol()

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
             padx=30,
             text=f'Machine precision: {sol}').grid(row=0)

def ex2_sol():
    u = ex1_sol()

    # Check sum associative
    x = 1.0
    y = u
    z = u

    if (x + y) + z != x + (y + z):
        sum_text = 'The operation \'+\' is not associative'
    else:
        sum_text = 'The operation \'+\' is associative'

    # Check product associative
    steps = 0
    while True:
        steps += 1
        x, y, z = random.random(), random.random(), random.random()
        if (x * y) * z != x * (y * z):
            prod_text = f'Product not associative for values: x={x}, y={y}, z={z}. '
            prod_text += f'Values found in {steps} steps'
            break

    return sum_text, prod_text

def ex2():
    global content
    content.destroy()

    text1, text2 = ex2_sol()

    content = tk.Frame()
    content.pack(side='left')
    tk.Label(content,
             padx=30,
             text=text1).grid(row=0)
    tk.Label(content, 
             padx=30,
             text=text2).grid(row=2)

def add(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def sub(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

# Pads matrices with 0 to closest power of 2
def pad(matrix):
    n = len(matrix)

    m = 1
    while m < n:
        m *= 2

    pad_matrix = [[0] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            pad_matrix[i][j] = matrix[i][j]
    return pad_matrix

# A, B have shape (n x n)
def strassen(A, B, nmin):
    A = pad(A)
    B = pad(B)

    n = len(A)

    if n <= nmin:
        return [[A[0][0] * B[0][0]]]
    
    # Split A and B into the 4 components
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    # Compute 7 sub-products recursively
    P1 = strassen(add(A11, A22), add(B11, B22), nmin)
    P2 = strassen(add(A21, A22), B11, nmin)
    P3 = strassen(A11, sub(B12, B22), nmin)
    P4 = strassen(A22, sub(B21, B11), nmin)
    P5 = strassen(add(A11, A12), B22, nmin)
    P6 = strassen(sub(A21, A11), add(B11, B12), nmin)
    P7 = strassen(sub(A12, A22), add(B21, B22), nmin)
    
    # Combine sub-products
    C11 = add(sub(add(P1, P4), P5), P7)
    C12 = add(P3, P5)
    C21 = add(P2, P4)
    C22 = add(sub(add(P1, P3), P2), P6)
    
    # Combine submatrices
    C = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]
    return C

# [[1,2],[3,4]],[[5,6],[7,8]]
# [[1,2,3],[4,5,6],[7,8,9]],[[10,11,12],[13,14,15],[16,17,18]]
def mul_matrices():
    A, B = eval(input_entry.get())
    C = strassen(A, B, 1)

    answer = '\n'.join([' '.join([str(cell) for cell in row]) for row in C])

    global content
    tk.Label(content,
             padx=30,
             text=answer).grid(row=4)

def ex3():
    global content
    content.destroy()

    global input_entry

    content = tk.Frame()
    content.pack(side='left')
    input_entry = tk.Entry(content,
             width=100)
    input_entry.grid(row=0, padx=30)
    tk.Button(content,
              text='Solve',
              padx=30,
              command=mul_matrices).grid(row=2)


window = tk.Tk()
window.geometry("800x500")

buttons = tk.Frame()
buttons.pack(side='top')
button1 = tk.Button(buttons,
                    text='Exercitiul 1',
                    width=20,
                    height=5,
                    command=ex1)
button1.grid(row=0, column=0)

button2 = tk.Button(buttons,
                    text='Exercitiul 2',
                    width=20,
                    height=5,
                    command=ex2)
button2.grid(row=0, column=1)

button3 = tk.Button(buttons,
                    text='Exercitiul 3',
                    width=20,
                    height=5,
                    command=ex3)
button3.grid(row=0, column=2)

content = tk.Frame()

window.mainloop()

