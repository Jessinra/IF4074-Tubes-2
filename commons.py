def euclidean_distance(a, b):
    square_total = 0
    for i in range(len(a)):
        square_total += (a[i] - b[i])**2
    return square_total ** 0.5