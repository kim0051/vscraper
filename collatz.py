def collatz(n):
    """ This function performs a collatz sequence
    on an integer n."""

    col = []

    while n != 1:
        if n % 2 == 0:
            n //= 2
            col.append(n)
        else:
            n = (n*3) + 1
            col.append(n)

    return col
