import numpy as np


def read_data(a_file, b_file):
    with open(a_file, 'r') as f:
        n = int(f.readline())
        a_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            a_matrix[i].append((val, j))

    with open(b_file, 'r') as f:
        n = int(f.readline())
        b_vector = []

        for line in f:
            val = float(line)
            b_vector.append(val)

    return (a_matrix, b_vector, n)


def is_zero(val, p):
    return abs(val) < pow(10, -p)


def are_equal(val1, val2, p):
    return abs(val1 - val2) < pow(10, -p)


def has_zero_diag(matrix):
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
        k_current += 1

        for i in range(n):
            sum = 0
            for (val, j) in a[i]:
                if j != i:
                    sum += val * x[j]
                else:
                    elem_diag = val

            new_x = (b[i] - sum) / elem_diag
            if not are_equal(new_x, x[i], p):
                sol_found = False

            x[i] = new_x

        if sol_found or k_current == k_max:
            break

    if not sol_found:
        return False
    else:
        return (x, k_current)


def compute_b_prime(a, sol, n):
    b_prime = [0 for i in range(n)]
    for i in range(n):
        for (val, j) in a[i]:
            b_prime[i] += val * sol[j]
    return b_prime


def get_norm(a, b, sol, n):
    a = np.array(a)
    b = np.array(b)
    sol = np.array(sol)

    b_prime = np.array(compute_b_prime(a, sol, n))
    return np.linalg.norm(b - b_prime)


# a, b, n = read_data('a_1.txt', 'b_1.txt')
# p = 7
# k_max = 1000
# sol, k_current = solve_gauss_seidel(a, b, n, p, k_max)
# print(len(sol))
# print(get_norm(a, b, sol, n))


def read_bonus_data(a_file, b_file, sum_file):
    with open(a_file, 'r') as f:
        n = int(f.readline())
        a_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            a_matrix[i].append((val, j))

    with open(b_file, 'r') as f:
        n = int(f.readline())
        b_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            b_matrix[i].append((val, j))

    with open(sum_file, 'r') as f:
        n = int(f.readline())
        sum_matrix = [[] for i in range(n)]

        for line in f:
            data = line.split(',')
            val = float(data[0])
            i = int(data[1])
            j = int(data[2])
            sum_matrix[i].append((val, j))

    return (a_matrix, b_matrix, sum_matrix, n)


def append_or_add(m, val, i, j):
    exists = False
    for index, (val_i, j_i) in enumerate(m[i]):
        if j_i == j:
            m[i][index] = (val_i + val, j)

            if (m[i][index][1] == 0):
                m[i].pop(index)

            exists = True
            break
    if not exists:
        m[i].append((val, j))


def compute_matrices_sum(m1, m2, n):
    m_sum = [[] for i in range(n)]
    for i in range(n):
        for (val, j) in m1[i]:
            append_or_add(m_sum, val, i, j)

        for (val, j) in m2[i]:
            append_or_add(m_sum, val, i, j)
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
    return True


a, b, sum, n = read_bonus_data('a.txt', 'b.txt', 'aplusb.txt')
absum = compute_matrices_sum(a, b, n)
p = 5
print(compare_matrices(sum, absum, n, p))
