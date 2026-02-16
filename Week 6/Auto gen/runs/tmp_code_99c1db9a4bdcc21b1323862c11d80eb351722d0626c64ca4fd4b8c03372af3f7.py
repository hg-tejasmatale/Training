def print_stars(num_stars: int):
    """
    Prints a specified number of stars on a single line.

    Args:
        num_stars: The integer number of stars to print.
    """
    if num_stars < 0:
        print("Number of stars cannot be negative.")
        return
    print("*" * num_stars)

if __name__ == "__main__":
    print("Printing 5 stars:")
    print_stars(5)

    print("\nPrinting 10 stars:")
    print_stars(10)

    print("\nPrinting 0 stars:")
    print_stars(0)

    print("\nPrinting 3 stars (using another method with a loop):")
    for _ in range(3):
        print("*", end="")
    print() # Newline after the loop

    print("\nPrinting a star pattern:")
    for i in range(1, 6):
        print_stars(i)
