import random
import sys
import numpy as np
import tkinter as tk


def read_matrix_from_file(file_name, p):
    with open(file_name, 'r') as f:
        n = int(f.readline())
        matrix = [[] for i in range(n)]

        for line in f:
            if line == '\n':
                break
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            append_or_add(matrix, val, i, j, p)
    return matrix


def generate_random_sym_sparse_matrix(n, p):
    matrix = [[] for i in range(n)]
    count = random.randint(n, 10*n)
    for k in range(count):
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        val = random.uniform(0, 100)
        append_or_add(matrix, val, i, j, p)
        append_or_add(matrix, val, j, i, p)
    return matrix


def append_or_add(m, val, i, j, p):
    exists = False
    for index, (val_i, j_i) in enumerate(m[i]):
        if j_i == j:
            m[i][index] = (val_i + val, j)

            if is_zero(m[i][index][0], p):
                m[i].pop(index)

            exists = True
            break
    if not exists:
        m[i].append((val, j))


def is_zero(val, p):
    return abs(val) < pow(10, -p)


def are_equal(val1, val2, p):
    return abs(val1 - val2) < pow(10, -p)


def is_symetric(matrix, p):
    for i_1 in range(len(matrix)):
        for (val_1, j_1) in matrix[i_1]:
            sym_found = False

            for (val_2, j_2) in matrix[j_1]:
                if j_2 == i_1 and are_equal(val_1, val_2, p):
                    sym_found = True

            if not sym_found:
                return False

    return True


def multiply_mat_vec(matrix, vector, n):
    result = [0 for i in range(n)]
    for i in range(n):
        for (val, j) in matrix[i]:
            result[i] += val * vector[j]
    return result


def solve_power_method(matrix, n, p, k_max):
    x_vec = [random.uniform(1, 10) for i in range(n)]
    norm_x = np.linalg.norm(x_vec)
    v = list(map(lambda x: 1 / norm_x * x, x_vec))

    w = multiply_mat_vec(matrix, v, n)
    delta = np.dot(np.array(w), np.array(v))
    k = 0

    while True:
        norm_w = np.linalg.norm(w)
        v = list(map(lambda w: 1 / norm_w * w, w))

        w = multiply_mat_vec(matrix, v, n)

        delta = np.dot(np.array(w), np.array(v))

        diff_norm = np.linalg.norm(np.array(w) - delta*np.array(v))
        k += 1
        if k >= k_max or diff_norm < n*pow(10, -p):
            break

    if k >= k_max:
        return (False, [], k)
    else:
        return (delta, v, k)


def read_bonus_matrix_from_file(file_name):
    with open(file_name, 'r') as f:
        n = int(f.readline())
        valori = []
        ind_col = []
        inceput_linii = [0 for i in range(n + 1)]
        current_i = 0

        for line in f:
            if line == '\n':
                break
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])

            if i != current_i:
                current_i += 1
                inceput_linii[current_i + 1] = inceput_linii[current_i]

            inceput_linii[current_i + 1] += 1

            valori.append(val)
            ind_col.append(j)

    return (valori, ind_col, inceput_linii)


def multiplt_struct_vec(valori, ind_col, inceput_linii, vector, n):
    result = [0 for i in range(n)]

    for i in range(1, n+1):
        for index in range(inceput_linii[i-1], inceput_linii[i]):
            val = valori[index]
            j = ind_col[index]
            result[i-1] += val * vector[j]
    return result


def solve_bonus_power_method(valori, ind_col, inceput_linii, n, p, k_max):
    x_vec = [random.uniform(1, 10) for i in range(n)]
    norm_x = np.linalg.norm(x_vec)
    v = list(map(lambda x: 1 / norm_x * x, x_vec))

    w = multiplt_struct_vec(valori, ind_col, inceput_linii, v, n)
    delta = np.dot(np.array(w), np.array(v))
    k = 0

    while True:
        norm_w = np.linalg.norm(w)
        v = list(map(lambda w: 1 / norm_w * w, w))
        w = multiplt_struct_vec(valori, ind_col, inceput_linii, v, n)

        delta = np.dot(np.array(w), np.array(v))

        diff_norm = np.linalg.norm(np.array(w) - delta*np.array(v))
        k += 1
        if k >= k_max or diff_norm < n*pow(10, -p):
            break

    if k >= k_max:
        return (False, [], k)
    else:
        return (delta, v, k)


def generate_normal_matrix(p, n):
    return np.random.rand(p, n)


def not_null_vals_count(S, p):
    count = 0
    for val in S:
        if not is_zero(val, p):
            count += 1
    return count


def get_cond_number(S, p):
    min = sys.maxsize
    max = 0
    for val in S:
        if not is_zero(val, p):
            if val > max:
                max = val
            if val < min:
                min = val
    return max/min


def calculate_svd(A, b, p):
    U, S, VT = np.linalg.svd(A, full_matrices=False)
    response = ""

    response += "Valorile singulare ale matricei A sunt: " + str(S) + ".\n"

    # rangul matricei A
    rank = np.linalg.matrix_rank(A)

    response += "Rangul matricei A (numpy) este: " + str(rank) + ".\n"
    response += "Rangul matricei A (calculat) este: " + \
        str(not_null_vals_count(S, p)) + ".\n"

    # numarul de conditionare al matricei A
    cond = np.linalg.cond(A)

    response += "Numarul de conditionare al matricei A (numpy) este: " + str(
        cond) + ".\n"
    response += "Numarul de conditionare al matricei A (calculat) este: " + str(
        get_cond_number(S, p)) + ".\n"

    # pseudoinversa Moore-Penrose a matricei A
    AI = VT.T @ np.linalg.inv(np.diag(S)) @ U.T

    response += "Pseudoinversa Moore-Penrose a matricei A este:\n"
    response += str(AI) + "\n"

    # solutia sistemului Ax = b
    xI = AI.dot(b)

    response += "Solutia sistemului Ax = b este:\n"
    response += str(xI) + "\n"

    # norma intre b si AxI
    norm_diff = np.linalg.norm(b - A.dot(xI), ord=2)

    response += "Norma de diferenta intre b si AxI este: " + \
        str(norm_diff) + ".\n"

    # pseudo-inversa in sensul celor mai mici patrate
    if np.linalg.det(A.T.dot(A)) == 0:
        response += "Nu se poate calcula pseudo-inversa in sensul celor mai mici patrate.\n"
        return response
    AJ = np.linalg.inv(A.T.dot(A)).dot(A.T)

    # norma intre AI si AJ
    norm_diff_A = np.linalg.norm(AI - AJ, ord=1)

    response += "Norma de diferenta intre matricele pseudoinverse AI si AJ este:" + \
        str(norm_diff_A) + ".\n"

    return response


def solve_normal_matrix():
    global p_n_values_entry
    global epsilon_entry
    global k_max_entry
    global bonus_text_entry
    global response_text
    global content

    response_text.destroy()
    p_n_vals = p_n_values_entry.get()
    m = int(epsilon_entry.get())

    ss = p_n_vals.split(",")
    p = int(ss[0].strip())
    n = int(ss[1].strip())

    A = generate_normal_matrix(p, n)
    b = generate_normal_matrix(p, 1)

    response = "Matrix A:\n" + str(A) + "\n Vector b:\n" + str(b) + "\n"

    response += calculate_svd(A, b, m)

    response_text = tk.Label(content,
                             padx=30,
                             text=response)
    response_text.grid(row=10)


def bullet_normal_matrix():
    global content
    content.destroy()

    global p_n_values_entry
    global epsilon_entry
    global k_max_entry
    global bonus_text_entry
    global response_text

    content = tk.Frame()
    content.pack(side='top')
    tk.Label(content,
             padx=30,
             text='p, n').grid(row=0)
    p_n_values_entry = tk.Entry(content,
                                width=50)
    p_n_values_entry.grid(row=1, padx=30)

    tk.Label(content,
             padx=30,
             text='m for epsilon <- 10^-m').grid(row=2)
    epsilon_entry = tk.Entry(content,
                             width=50)
    epsilon_entry.grid(row=3, padx=30)

    tk.Button(content,
              text='SOLVE',
              padx=30,
              width=34,
              command=solve_normal_matrix).grid(row=8)

    response_text = tk.Label(content,
                             padx=30,
                             text='')
    response_text.grid(row=10)


def solve_square_matrix():
    global file_name_entry
    global epsilon_entry
    global k_max_entry
    global bonus_text_entry
    global response_text
    global content

    response_text.destroy()

    p = int(epsilon_entry.get())
    k_max = int(k_max_entry.get())
    file_name = file_name_entry.get()
    bonus_bool = bonus_text_entry.get()

    if bonus_bool.strip() != "true":
        if file_name.startswith("random:"):
            ss = file_name.split("random:")[1].split(",")
            n = int(ss[0].strip())
            a = generate_random_sym_sparse_matrix(n, p)
        else:
            a = read_matrix_from_file(file_name, p)

        if not is_symetric(a, p):
            response_text = tk.Label(content,
                                     padx=30,
                                     text='Matrix is not symmetric, Abort!')
            response_text.grid(row=10)
            return

        delta, v, k_current = solve_power_method(a, len(a), p, k_max)
    else:
        valori, ind_col, inceput_linii = read_bonus_matrix_from_file(file_name)

        delta, v, k_current = solve_bonus_power_method(
            valori, ind_col, inceput_linii, len(inceput_linii) - 1, p, k_max)

    if delta != False:
        response = f"Valoare proprie maxima: {delta} gasita la pasul {k_current}."
        response_text = tk.Label(content,
                                 padx=30,
                                 text=response)
        response_text.grid(row=10)
    else:
        response = f"Valoare proprie maxima nu a putut fi gasita, {k_current} pasi atinsi."
        response_text = tk.Label(content,
                                 padx=30,
                                 text=response)
        response_text.grid(row=10)


def bullet_square_matrix():
    global content
    content.destroy()

    global file_name_entry
    global epsilon_entry
    global k_max_entry
    global bonus_text_entry
    global response_text

    content = tk.Frame()
    content.pack(side='top')
    tk.Label(content,
             padx=30,
             text='matrix file name ("random: n" for runtime generation)').grid(row=0)
    file_name_entry = tk.Entry(content,
                               width=50)
    file_name_entry.grid(row=1, padx=30)

    tk.Label(content,
             padx=30,
             text='m for epsilon <- 10^-m').grid(row=2)
    epsilon_entry = tk.Entry(content,
                             width=50)
    epsilon_entry.grid(row=3, padx=30)

    tk.Label(content,
             padx=30,
             text='k max value').grid(row=4)
    k_max_entry = tk.Entry(content,
                           width=50)
    k_max_entry.grid(row=5, padx=30)

    tk.Label(content,
             padx=30,
             text='bonus ("true/false")').grid(row=6)
    bonus_text_entry = tk.Entry(content,
                                width=50)
    bonus_text_entry.grid(row=7, padx=30)

    tk.Button(content,
              text='SOLVE',
              padx=30,
              width=34,
              command=solve_square_matrix).grid(row=8)

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
                        text='Square Matrix',
                        width=20,
                        height=5,
                        command=bullet_square_matrix)
    button1.grid(row=0, column=0)

    button2 = tk.Button(buttons,
                        text='Normal Matrix',
                        width=20,
                        height=5,
                        command=bullet_normal_matrix)
    button2.grid(row=0, column=1)

    content = tk.Frame()

    window.mainloop()


gui()
