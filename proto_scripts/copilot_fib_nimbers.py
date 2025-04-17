from functools import lru_cache

def generate_fibonacci(n):
    """
    Generate the first n Fibonacci numbers.

    :param n: Number of Fibonacci numbers to generate
    :return: List of the first n Fibonacci numbers
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fibonacci_sequence = [0, 1]
    for _ in range(2, n):
        fibonacci_sequence.append(fibonacci_sequence[-1] + fibonacci_sequence[-2])
    return fibonacci_sequence

@lru_cache(maxsize=None)
def fibonacci_recursive(n):
    """
    Optimized recursive function to calculate the nth Fibonacci number using memoization.

    :param n: The position of the Fibonacci number to calculate
    :return: The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)



# Example usage
if __name__ == "__main__":
    n = 10  # Change this value to generate a different number of Fibonacci numbers
    print(generate_fibonacci(n))
    # Example usage of the recursive function
    for i in range(n):
        print(f"Fibonacci number {i}: {fibonacci_recursive(i)}")
# This script generates Fibonacci numbers and includes a recursive function to calculate the nth Fibonacci number.
# Створення списку чисел фібоначі за допомогою рекурсивної функції

# Створення списку чисел фібоначі за допомогою рекурсивної функції
fib_n = [fibonacci_recursive(i) for i in range(10)]  # Змінити значення для генерації іншої кількості чисел фібоначі
print(fib_n)  # Вивід списку чисел фібоначі 
    

