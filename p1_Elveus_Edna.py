"""Solves quadratic equations and plots them."""

from matplotlib import pyplot as plt


while True:
    a = (input("Enter a: "))
    if a == "":
        break

    b = float(input("Enter b: "))
    c = float(input("Enter c: "))
    a = float(a)

    determinant = b**2 - 4*a*c

    if determinant < 0:
        print("no real solutions")
    elif determinant == 0:
        x1 = -b / (2*a)
        print(f"one solution: {x1:.5f}")
    else:
        x1 = (-b - determinant**0.5) / (2*a)
        x2 = (-b + determinant**0.5) / (2*a)
        print(f"two solutions: x1={x1:.5f} x2={x2:.5f}")

    if determinant > 0:
        root_min = min(x1, x2)
        root_max = max(x1, x2)

        margin = (root_max - root_min) + 1

        x_min = root_min - margin
        x_max = root_max + margin
    elif determinant == 0:
        x_opt = -b / (2*a)
        margin = 2
        x_min = x_opt - margin
        x_max = x_opt + margin
    else:
        x_opt = -b / (2*a)
        margin = 5
        x_min = x_opt - margin
        x_max = x_opt + margin

    points = 150
    step = (x_max - x_min) / (points - 1)
    xs = [x_min + i * step for i in range(points)]

    ys = [a * x**2 + b * x + c for x in xs]

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Graph of {a}x^2 + {b}x + {c}")
    plt.show()
