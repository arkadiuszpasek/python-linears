# Placeholder for the assignment, refer to the example.py for tips
# How to use SAPORT?

# 1. Import the library
from saport.simplex.model import Model

# 2. Create a model
model = Model("Zad1")

# 3. Add variables
x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")
x4 = model.create_variable("x4")

# 4. FYI: You can create expression and evaluate them
# expr2 = 0.16 * x1 - 0.94 * x2 + 0.9 * x3

# 5. Then add constraints to the model
model.add_constraint(0.8 * x1 + 2.4 * x2 + 0.9 * x3 + 0.4 * x4 >= 1200)
model.add_constraint(0.6 * x1 + 0.6 * x2 + 0.3 * x3 + 0.3 * x4 >= 600)

# 6. Set the objective!
model.maximize(-9.6 * x1 - 14.4 * x2 - 10.8 * x3 - 7.2 * x4)

# 7. You can print the model
print("Before solving:")
print(model)

# 8. And finally solve it!
solution = model.solve()

# 9. Model is being simplified before being solver
print("After solving:")
print(model)

# 10. Print solution (uncomment after finishing assignment)
print("Solution: ")
print(solution)
