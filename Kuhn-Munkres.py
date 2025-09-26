import numpy as np

def kuhn_munkres_algorithm(cost_matrix):
    cost_matrix = np.array(cost_matrix)
    n, m = cost_matrix.shape

    # Ensure the matrix is square by padding with large values
    size = max(n, m)
    max_num = np.max(cost_matrix) + 1
    padded_matrix = np.full((size, size), max_num)
    padded_matrix[:n, :m] = cost_matrix

    u = np.zeros(size)
    v = np.zeros(size)
    p = np.full(size, -1, dtype=int)


    for i in range(size):
        links = np.full(size, -1, dtype=int)
        mins = np.full(size, np.inf)
        visited = np.zeros(size, dtype=bool)
        marked_i = i
        marked_j = -1
        while True:
            j = -1
            for j1 in range(size):
                if not visited[j1]:
                    cur = padded_matrix[marked_i, j1] - u[marked_i] - v[j1]
                    if cur < mins[j1]:
                        mins[j1] = cur
                        links[j1] = marked_j
                    if j == -1 or mins[j1] < mins[j]:
                        j = j1
            delta = mins[j]
            for j1 in range(size):
                if visited[j1]:
                    u[p[j1]] += delta
                    v[j1] -= delta
                else:
                    mins[j1] -= delta
            u[i] += delta
            visited[j] = True
            marked_j = j
            marked_i = p[j]
            if marked_i == -1:
                break
        while True:
            if links[j] != -1:
                p[j] = p[links[j]]
                j = links[j]
            else:
                break
        p[j] = i

    result = np.full(size, -1, dtype=int)
    for j in range(size):
        if p[j] != -1:
            result[p[j]] = j

    # Extract the actual assignments and calculate the cost
    actual_assignment = result[:n]
    actual_cost = 0
    for i in range(n):
        if actual_assignment[i] != 3:
            actual_cost += cost_matrix[i][actual_assignment[i]]
    
    for task in range(n):
        if actual_assignment[task] < m:
            print(f"Task[{task+1}] assigned to Processor[{actual_assignment[task]+1}]")
        else:
            print(f"Task[{task+1}] assigned to a dummy processor")

    return actual_assignment, actual_cost

# ------------------test---------------------
n = 4  # tasks_cnt
m = 3  # processors_cnt

cost_matrix = [
    [9, 2, 7],
    [6, 4, 3],
    [5, 8, 1],
    [7, 6, 2]
]


assignment, cost = kuhn_munkres_algorithm(cost_matrix)
print("Minimum Time:", cost)
