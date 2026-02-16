def fibonacci(n: int) -> int:
    """
    Calculates the nth Fibonacci number iteratively.

    The Fibonacci sequence starts with F(0) = 0 and F(1) = 1.
    F(n) = F(n-1) + F(n-2) for n > 1.

    Args:
        n: The index of the desired Fibonacci number (non-negative integer).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is a negative integer.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def fibonacci_sequence(n: int):
    """
    Generates the first n Fibonacci numbers.

    Args:
        n: The number of Fibonacci numbers to generate (non-negative integer).

    Yields:
        The next Fibonacci number in the sequence.

    Raises:
        ValueError: If n is a negative integer.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    a, b = 0, 1
    for i in range(n):
        if i == 0:
            yield 0
        elif i == 1:
            yield 1
        else:
            a, b = b, a + b
            yield b

if __name__ == "__main__":
    print("--- Nth Fibonacci Number ---")
    # Test cases for fibonacci(n)
    print(f"fibonacci(0): {fibonacci(0)}")
    print(f"fibonacci(1): {fibonacci(1)}")
    print(f"fibonacci(2): {fibonacci(2)}")
    print(f"fibonacci(3): {fibonacci(3)}")
    print(f"fibonacci(4): {fibonacci(4)}")
    print(f"fibonacci(5): {fibonacci(5)}")
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"fibonacci(20): {fibonacci(20)}")

    try:
        fibonacci(-1)
    except ValueError as e:
        print(f"Error calling fibonacci(-1): {e}")

    print("\n--- Fibonacci Sequence Generator ---")
    # Test cases for fibonacci_sequence(n)
    print("First 0 numbers:", list(fibonacci_sequence(0)))
    print("First 1 number:", list(fibonacci_sequence(1)))
    print("First 5 numbers:", list(fibonacci_sequence(5)))
    print("First 10 numbers:", list(fibonacci_sequence(10)))

    try:
        list(fibonacci_sequence(-1))
    except ValueError as e:
        print(f"Error calling fibonacci_sequence(-1): {e}")

