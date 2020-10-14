from enum import Enum
from functools import reduce 

class ObjectiveType(Enum):
    """
        An enum to represent an objective type:
        - MAX = maximize the objective
        - MIN = minimze the objective
    """
    MAX = 1
    MIN = -1

    def __str__(self):
        return {
            ObjectiveType.MAX: 'max',
            ObjectiveType.MIN: 'min'
        }[self]

class Objective: 
    """
        A class to represent an objective in the linear programming expression, e.g. 4x + 5y -> max, etc.

        Attributes
        ----------
        expression : Expression
            polynomial expressions that is being optimized
        type: ObjectiveType
            type of the objective: MIN, MAX

        Methods
        -------
        __init__(expression: Expression, type: ObjectiveType = ObjectiveType.Max) -> Constraint:
            constructs new objective with a specified polynomial and type
        simplify() -> Objective:
            returns new objective with the simplified polynomial
        evaluate(assignemnt: list[float]) -> float:
            returns value of the objective for the given assignment
            assignment is just a list of floats corresponding (by index) to the variables in the model 
    """

    def __init__(self, expression, type = ObjectiveType.MAX):
        self.expression = expression
        self.type = type
        
    def simplify(self):
        return Objective(self.expression.simplify(), self.type)

    def evaluate(self, assignment):
        return self.expression.evaluate(assignment)
        
    def __str__(self):
        return f'{self.expression} -> {self.type}'