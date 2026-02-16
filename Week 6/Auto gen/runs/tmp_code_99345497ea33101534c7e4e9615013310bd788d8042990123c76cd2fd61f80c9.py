def print_stars():
    """
    Prints various patterns of stars to the console.
    """
    print("--- Star Printer Script ---")
    print("\nPattern 1: A simple line of stars")
    print("*" * 20) # Prints 20 stars

    print("\nPattern 2: A square of stars")
    square_size = 5
    for _ in range(square_size):
        print("*" * square_size)

    print("\nPattern 3: A right-angled triangle of stars")
    triangle_height = 7
    for i in range(1, triangle_height + 1):
        print("*" * i)

    print("\nPattern 4: An inverted right-angled triangle of stars")
    for i in range(triangle_height, 0, -1):
        print("*" * i)

    print("\nPattern 5: A pyramid of stars")
    pyramid_height = 6
    for i in range(pyramid_height):
        # Calculate leading spaces and stars for each row
        spaces = " " * (pyramid_height - i - 1)
        stars = "*" * (2 * i + 1)
        print(spaces + stars)

    print("\n--- Script Finished ---")

if __name__ == "__main__":
    print_stars()
