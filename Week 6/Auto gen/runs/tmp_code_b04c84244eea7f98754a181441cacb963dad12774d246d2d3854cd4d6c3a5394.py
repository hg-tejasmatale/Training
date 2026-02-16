def print_stars(count):
    """
    Prints a specified number of stars on a single line.

    Args:
        count (int): The number of stars to print.
    """
    if count < 0:
        print("Star count cannot be negative.")
        return
    print("*" * count)

if __name__ == "__main__":
    print("Printing 5 stars:")
    print_stars(5)

    print("\nPrinting 10 stars:")
    print_stars(10)

    print("\nPrinting 0 stars:")
    print_stars(0)

    print("\nPrinting a pyramid of stars:")
    for i in range(1, 6):
        print_stars(i)

    print("\nPrinting a reverse pyramid of stars:")
    for i in range(5, 0, -1):
        print_stars(i)
