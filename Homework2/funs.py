# File with sample functions.
def sum(x, y): # sums up two numbers
    """ Adds two numbers.
    Returns the sum."""
    return x + y

# Returns the product.
def mul(x, y): # multiplies two numbers
    # z is a local variable
    z = x * y
    return z

def print_pretty(a):
    print("The result is {:.3f}.".format(a))

# test these functions:
print_pretty(mul(10, sum(3, 5)))