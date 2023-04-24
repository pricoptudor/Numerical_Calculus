import numpy as np
import tkinter as tk


def read_data(a_file, b_file, p):
    with open(a_file, 'r') as f:
        n = int(f.readline())
        a_matrix = [[] for i in range(n)]

        for line in f:
            if line == '\n':
                break
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            append_or_add(a_matrix, val, i, j, p)

    with open(b_file, 'r') as f:
        n = int(f.readline())
        b_vector = []

        for line in f:
            if line == '\n':
                break
            val = float(line)
            b_vector.append(val)

    return (a_matrix, b_vector, n)


def append_or_add(m, val, i, j, p):
    exists = False
    for index, (val_i, j_i) in enumerate(m[i]):
        if j_i == j:
            m[i][index] = (val_i + val, j)

            if is_zero(m[i][index][1], p):
                m[i].pop(index)

            exists = True
            break
    if not exists:
        m[i].append((val, j))


def is_zero(val, p):
    return abs(val) < pow(10, -p)


def are_equal(val1, val2, p):
    return abs(val1 - val2) < pow(10, -p)


def has_not_zero_diag(matrix):
    for i in range(len(matrix)):
        ok = False
        for j in matrix[i]:
            if j[1] == i:
                ok = True
        if ok == False:
            return False
    return True


def solve_gauss_seidel(a, b, n, p, k_max):
    x = [0 for i in range(n)]
    k_current = 0
    while True:
        sol_found = True
        exceeded_delta = False
        k_current += 1
        current_delta = 0

        for i in range(n):
            sum = 0
            for (val, j) in a[i]:
                if j != i:
                    sum += val * x[j]
                else:
                    elem_diag = val

            new_x = (b[i] - sum) / elem_diag

            current_delta += abs(new_x - x[i])

            x[i] = new_x

        if not is_zero(current_delta, p):
            sol_found = False

        if current_delta > pow(10, 8):
            exceeded_delta = True

        if sol_found or k_current == k_max or exceeded_delta:
            break

    if not sol_found:
        if k_current == k_max:
            return (False, f"Solution not found, K (steps) reached {k_max}.")

        if exceeded_delta:
            return (False, f"Solution not found, Delta reached {pow(10, 8)} at step k = {k_current}.")

    else:
        return (x, f"Solution found at step k = {k_current}.")


def compute_b_prime(a, sol, n):
    b_prime = [0 for i in range(n)]
    for i in range(n):
        for (val, j) in a[i]:
            b_prime[i] += val * sol[j]
    return b_prime


def get_norm(a, b, sol, n):
    b = np.array(b)
    sol = np.array(sol)

    b_prime = np.array(compute_b_prime(a, sol, n))
    return np.linalg.norm(b - b_prime)


def solve_homework():
    global a_file_entry
    global b_file_entry
    global epsilon_entry
    global k_max_entry
    global response_text
    global content

    response_text.destroy()

    p = int(epsilon_entry.get())
    k_max = int(k_max_entry.get())
    a, b, n = read_data(a_file_entry.get(), b_file_entry.get(), p)

    if not has_not_zero_diag(a):
        response_text = tk.Label(content,
                                 padx=30,
                                 text='Diagonal is 0, Abort!')
        response_text.grid(row=10)
        return

    sol, response = solve_gauss_seidel(a, b, n, p, k_max)
    if sol != False:
        norm = get_norm(a, b, sol, n)
        response_text = tk.Label(content,
                                 padx=30,
                                 text=response + '\n' + f'The Norm is {norm}')
        response_text.grid(row=10)
    else:
        response_text = tk.Label(content,
                                 padx=30,
                                 text=response)
        response_text.grid(row=10)


def bullet_homework():
    global content
    content.destroy()

    global a_file_entry
    global b_file_entry
    global epsilon_entry
    global k_max_entry
    global response_text

    content = tk.Frame()
    content.pack(side='top')
    tk.Label(content,
             padx=30,
             text='first file name').grid(row=0)
    a_file_entry = tk.Entry(content,
                            width=50)
    a_file_entry.grid(row=1, padx=30)

    tk.Label(content,
             padx=30,
             text='second file name').grid(row=2)
    b_file_entry = tk.Entry(content,
                            width=50)
    b_file_entry.grid(row=3, padx=30)

    tk.Label(content,
             padx=30,
             text='m for epsilon <- 10^-m').grid(row=4)
    epsilon_entry = tk.Entry(content,
                             width=50)
    epsilon_entry.grid(row=5, padx=30)

    tk.Label(content,
             padx=30,
             text='k max value').grid(row=6)
    k_max_entry = tk.Entry(content,
                           width=50)
    k_max_entry.grid(row=7, padx=30)

    tk.Button(content,
              text='SOLVE',
              padx=30,
              width=34,
              command=solve_homework).grid(row=9)

    response_text = tk.Label(content,
                             padx=30,
                             text='')
    response_text.grid(row=10)


def read_bonus_data(a_file, b_file, sum_file, p):
    with open(a_file, 'r') as f:
        n = int(f.readline())
        a_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            append_or_add(a_matrix, val, i, j, p)

    with open(b_file, 'r') as f:
        n = int(f.readline())
        b_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            append_or_add(b_matrix, val, i, j, p)

    with open(sum_file, 'r') as f:
        n = int(f.readline())
        sum_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            append_or_add(sum_matrix, val, i, j, p)

    return (a_matrix, b_matrix, sum_matrix, n)


def compute_matrices_sum(m1, m2, n, p):
    m_sum = [[] for i in range(n)]
    for i in range(n):
        for (val, j) in m1[i]:
            append_or_add(m_sum, val, i, j, p)

        for (val, j) in m2[i]:
            append_or_add(m_sum, val, i, j, p)
    return m_sum


def compare_matrices(m1, m2, n, p):
    for i in range(n):
        for (val_1, j_1) in m1[i]:
            equal = False

            for (val_2, j_2) in m2[i]:
                if j_1 == j_2 and are_equal(val_1, val_2, p):
                    equal = True

            if not equal:
                return False
            
        for (val_2, j_2) in m2[i]:
            equal = False

            for (val_1, j_1) in m1[i]:
                if j_2 == j_1 and are_equal(val_2, val_1, p):
                    equal = True

            if not equal:
                return False
    return True


def solve_bonus():
    global a_file_entry
    global b_file_entry
    global sum_file_entry
    global epsilon_entry
    global response_text
    global content

    response_text.destroy()

    p = int(epsilon_entry.get())
    a, b, sum, n = read_bonus_data(
        a_file_entry.get(), b_file_entry.get(), sum_file_entry.get(), p)

    computed_sum = compute_matrices_sum(a, b, n, p)
    if compare_matrices(sum, computed_sum, n, p):
        response_text = tk.Label(content,
                                 padx=30,
                                 text="The Sum of the 2 Matrices is equal to the Matrix from the Sum File.")
        response_text.grid(row=10)
    else:
        response_text = tk.Label(content,
                                 padx=30,
                                 text="The Sum of the 2 Matrices is NOT equal to the Matrix from the Sum File.")
        response_text.grid(row=10)


def bullet_bonus():
    global content
    content.destroy()

    global a_file_entry
    global b_file_entry
    global sum_file_entry
    global epsilon_entry
    global response_text

    content = tk.Frame()
    content.pack(side='top')
    tk.Label(content,
             padx=30,
             text='first file name').grid(row=0)
    a_file_entry = tk.Entry(content,
                            width=50)
    a_file_entry.grid(row=1, padx=30)

    tk.Label(content,
             padx=30,
             text='second file name').grid(row=2)
    b_file_entry = tk.Entry(content,
                            width=50)
    b_file_entry.grid(row=3, padx=30)

    tk.Label(content,
             padx=30,
             text='sum file name').grid(row=4)
    sum_file_entry = tk.Entry(content,
                              width=50)
    sum_file_entry.grid(row=5, padx=30)

    tk.Label(content,
             padx=30,
             text='m for epsilon <- 10^-m').grid(row=6)
    epsilon_entry = tk.Entry(content,
                             width=50)
    epsilon_entry.grid(row=7, padx=30)

    tk.Button(content,
              text='SOLVE',
              padx=30,
              width=34,
              command=solve_bonus).grid(row=9)

    response_text = tk.Label(content,
                             padx=30,
                             text='')
    response_text.grid(row=10)


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

    button2 = tk.Button(buttons,
                        text='Bonus',
                        width=20,
                        height=5,
                        command=bullet_bonus)
    button2.grid(row=0, column=1)

    content = tk.Frame()

    window.mainloop()


gui()
