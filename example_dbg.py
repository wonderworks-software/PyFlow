# Example Python Program for PyFlow Visual Debugger
# This file demonstrates various Python constructs that can be 
# converted into visual nodes

# ============================================
# Example 1: Simple Variables and Math
# ============================================
x = 10
y = 20
result = x + y
print(f"Sum: {result}")

# ============================================
# Example 2: List Operations
# ============================================
numbers = [5, 2, 8, 1, 9, 3]
max_value = numbers[0]

# Find maximum using a loop
for i in range(1, len(numbers)):
    if numbers[i] > max_value:
        max_value = numbers[i]

print(f"Maximum value: {max_value}")

# ============================================
# Example 3: Function Definition
# ============================================
def calculate_average(data):
    """Calculate the average of a list of numbers."""
    if len(data) == 0:
        return 0
    total = 0
    for num in data:
        total = total + num
    return total / len(data)

average = calculate_average(numbers)
print(f"Average: {average}")

# ============================================
# Example 4: Conditional Logic
# ============================================
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score {score} = Grade {grade}")

# ============================================
# Example 5: While Loop
# ============================================
counter = 0
total = 0

while counter < 5:
    total = total + counter
    counter = counter + 1

print(f"Sum of 0 to 4: {total}")

# ============================================
# Example 6: String Operations
# ============================================
message = "Hello, PyFlow!"
uppercase = message.upper()
length = len(message)
print(f"Message: {message}")
print(f"Uppercase: {uppercase}")
print(f"Length: {length}")

# ============================================
# Example 7: Dictionary Usage
# ============================================
student = {
    "name": "Alice",
    "age": 20,
    "grades": [85, 90, 78]
}

student_name = student["name"]
student_age = student["age"]
print(f"Student: {student_name}, Age: {student_age}")

# ============================================
# Example 8: Nested Loops (Matrix)
# ============================================
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

diagonal_sum = 0
for i in range(3):
    diagonal_sum = diagonal_sum + matrix[i][i]

print(f"Diagonal sum: {diagonal_sum}")

# ============================================
# Example 9: Class Definition
# ============================================
class Calculator:
    def __init__(self, name):
        self.name = name
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

calc = Calculator("MyCalc")
sum_result = calc.add(5, 3)
product = calc.multiply(4, 7)
print(f"5 + 3 = {sum_result}")
print(f"4 * 7 = {product}")

# ============================================
# Example 10: List Comprehension
# ============================================
squares = [n * n for n in range(1, 6)]
even_squares = [s for s in squares if s % 2 == 0]
print(f"Squares: {squares}")
print(f"Even squares: {even_squares}")

# ============================================
# Final Output
# ============================================
print("\n=== Program Complete ===")
