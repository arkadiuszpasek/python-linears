# Placeholder for the assignment, refer to the example.py for tips 
# How to use SAPORT?

# 1. Import the library
from saport.simplex.model import Model 

# 2. Create a model
model = Model("2")

# 3. Add variables
x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")
x4 = model.create_variable("x4")

# 4. FYI: You can create expression and evaluate them
# expr2 = 0.16 * x1 - 0.94 * x2 + 0.9 * x3

# 5. Then add constraints to the model
model.add_constraint(2.0 * x1 + 4.0 * x2 + 3.0 * x3 + 7.0 * x4 <= 800)
model.add_constraint(4.0 * x1 + 5.0 * x2 + 3.0 * x3 + 2.0 * x4 <= 640)
model.add_constraint(4.0 * x1 + 1.0 * x2 + 4.0 * x3 + 1.0 * x4 <= 600)

# 6. Set the objective!
model.maximize(80.0* x1 + 60.0*x2 + 30.0*x3 + 50.0 * x4)

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





