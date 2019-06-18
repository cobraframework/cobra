import random

numbers = '1029384756'


# Generate random numbers by default size is 32
def generate_numbers(size=32):
    string = []
    for _ in range(1, size + 1):
        string.append(random.choice(numbers))
    return str().join(string)
