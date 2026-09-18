"""
Function Plotter
Problem 4 - CS Assignment
"""

import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    """
    Plot a mathematical function defined by a string expression.
    
    Computes ns evenly spaced points across the domain, evaluates the
    function at each point using eval(), displays a table of values,
    and generates a plot of the function.
    
    Args:
        fun_str (str): String expression like "2 * x + 3" or "math.sin(x)"
        domain (tuple): (xmin, xmax) defining the range
        ns (int): Number of sample points to use
    """
    xmin, xmax = domain
    
    # Generate ns evenly spaced points across [xmin, xmax]
    if ns > 1:
        step = (xmax - xmin) / (ns - 1)
    else:
        step = 0
    
    xs = []
    for i in range(ns):
        xs.append(xmin + i * step)
    
    # Evaluate function at each x using eval()
    ys = []
    for x in xs:
        # eval() will see x in the local scope
        y = eval(fun_str)
        ys.append(y)
    
    # Display table of values
    print("        x        y")
    for i in range(ns):
        # Format: 4 decimal places with + sign for positive values
        print(f"{xs[i]:+8.4f} {ys[i]:+8.4f}")
    
    # Plot the function
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Function: {fun_str}")
    plt.grid(True, alpha=0.3)
    plt.show()


def main():
    """
    Main program: reads function string, domain, and number of samples,
    then calls plot_function.
    """
    print("Function Plotter")
    print("-" * 40)
    
    # Read inputs from terminal
    fun_str = input("Enter function (e.g., '2 * x + 3'): ")
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))
    ns = int(input("Enter number of samples: "))
    
    # Validate inputs
    if ns <= 0:
        print("Number of samples must be positive.")
        return
    
    if xmin >= xmax:
        print("xmin must be less than xmax.")
        return
    
    # Call plot_function
    plot_function(fun_str, domain=(xmin, xmax), ns=ns)


# Run the program
if __name__ == "__main__":
    main()