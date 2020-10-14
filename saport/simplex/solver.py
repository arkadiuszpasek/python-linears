import numpy
from copy import deepcopy
from saport.simplex.expressions.objective import ObjectiveType
from saport.simplex.expressions.constraint import ConstraintType
class Solution:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the solution
        assignment : list[float]
            list with the values assigned to the variables
            order of values should correspond to the order of variables in model.variables list


        Methods
        -------
        __init__(model: Model, assignment: list[float]) -> Solution:
            constructs a new solution for the specified model and assignment
        value(var: Variable) -> float:
            returns a value assigned to the specified variable
        objective_value()
            returns value of the objective function
    """

    def __init__(self, model, assignment):
        "Assignment is just a list of values"
        self.assignment = assignment
        self.model = model

    def value(self, var):
        return self.assignment[var.index]

    def objective_value(self):
        return self.model.objective.evaluate(self.assignment)       

    def __str__(self):
        text = f'- objective value: {self.objective_value()}\n'
        text += '- assignment:\n'
        for (i,var) in enumerate(self.assignment):
            text += f'\t {self.model.variables[i].name} : {self.assignment[var]}'
        return text

class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """
    def __init__(self):
        self.extraVars = []

    def solve(self, model):
        normal_model = self._normalize_model(deepcopy(model))
        solution = self._find_initial_solution(normal_model)
        tableaux = self._tableux(normal_model, solution)
        #TODO: 
        print("--- Normalized model ---")
        print(normal_model)
        print("--- Initial Solution ---")
        print()
        # - print initial solution
        # - print tableux
        return normal_model
        # return solution

    def _normalize_model(self, model):
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """
        #TODO: this method should create a new canonical model based on the current one
        # - canonical model has only the MAX objective
        # - canonical model has only EQ constraints (thanks to the additional slack / surplus variables)
        #   you should add extra (slack, surplus) variables and store them somewhere as the solver attribute
        if model.objective.type != ObjectiveType.MAX:
            raise Exception("Not max")
        model.name = f"Normalized {model.name}"
        constraints = model.constraints
        model.constraints = model.constraints[:len(model.variables)]
        for index, c in enumerate(constraints):
            if index < len(model.variables):
                continue
            variable = model.create_variable(f"s{index}")
            if c.type == ConstraintType.LE or c.type == ConstraintType.EQ:
                model.add_constraint(c.expression + 1.0 * variable == c.bound)
            elif c.type == ConstraintType.GE:
                model.add_constraint(c.expression - 1.0 * variable == c.bound)

            variable.factor = 0
            self.extraVars.append(variable)
        return model

    def _find_initial_solution(self, model):
        """
        _find_initial_solution(model: Model) -> Solution
            returns an initial solution for the given model
        """
        #TODO: this method should find an initial feasible solution to the model
        # - should use the slack / surplus variables added during the normalization

        ### prepare arrays
        objective_atoms = model.objective.expression.atoms
        constraintsValues = []
        bi = []
        cj = []
        non_ge_zero_constraints = []
        for i in range(len(model.variables)):
            if i >= len(objective_atoms):
                cj.append(0)
            else:
                cj.append(objective_atoms[i].factor)

        for i in range(len(model.constraints)):
            if len(model.constraints[i].expression.atoms) == 1 and model.constraints[i].bound == 0:
                continue
            else:
                non_ge_zero_constraints.append(model.constraints[i])

        for j in range(len(self.extraVars)):
            bi.append(non_ge_zero_constraints[j].bound)
            constraintValues = []
            atoms = non_ge_zero_constraints[j].expression.atoms
            for i in range(len(model.variables)):
                maybe_value = None
                for a in range(len(atoms)):
                    if model.variables[i].name == atoms[a].var.name:
                        maybe_value = atoms[a].factor
                        break
                if maybe_value != None:
                    constraintValues.append(maybe_value)
                    continue

                if i >= len(atoms) -1:
                    constraintValues.append(0)
                    continue
            constraintsValues.append(constraintValues)


        ### Keep looking for best solution
        while True:
            ### Calculate loop current vars
            zj = []
            for i in range(len(cj)):
                zCurrent = 0
                for j in range(len(self.extraVars)):
                    zCurrent += self.extraVars[j].factor * constraintsValues[j][i]
                zj.append(zCurrent)

            delta_z = []
            shouldFinish = True
            for i in range(len(cj)):
                delta_z.append(cj[i] - zj[i])
                if cj[i] - zj[i] > 0:
                    shouldFinish = False
            if shouldFinish:
                print("breaking")
                print(self.extraVars[0])
                print(self.extraVars[2])
                print(self.extraVars[1])
                print(bi)
                print(constraintsValues[0])
                print(constraintsValues[1])
                print(constraintsValues[2])
                break
            current_col_ind = _find_max_index(delta_z)
            bi_calc = []
            for i in range(len(bi)):
                try:
                    val = bi[i] / constraintsValues[i][current_col_ind]
                    if val > 0:
                        bi_calc.append(val) 
                    else:
                        bi_calc.append(9999999) ## TODO: Make type for ignored value
                except ZeroDivisionError:
                    bi_calc.append(99999999)

            current_row_ind = _find_min_index(bi_calc)

            ### Transform to next iteration

            swap_var = model.variables[current_col_ind]
            swap_var.factor = cj[current_col_ind]

            new_constr_values = []

            self.extraVars[current_row_ind] = swap_var
            for i in range(len(self.extraVars)):
                current_row = []
                if i == current_row_ind:
                    for j in range(len(cj)):
                        current_v = constraintsValues[i][j] / constraintsValues[current_row_ind][current_col_ind]
                        current_row.append(current_v)
                else:
                    for j in range(len(cj)):
                        current_v = constraintsValues[i][j] - \
                        ((constraintsValues[i][current_col_ind] * constraintsValues[current_row_ind][j]) \
                        / constraintsValues[current_row_ind][current_col_ind])
                        
                        current_row.append(current_v)
                new_constr_values.append(current_row)
            
            new_bi = []
            for i in range(len(self.extraVars)):
                if i == current_row_ind:
                    current_v = bi[i] / constraintsValues[current_row_ind][current_col_ind]
                    new_bi.append(current_v)
                else:
                    current_v = bi[i] - (constraintsValues[i][current_col_ind] * bi[current_row_ind]\
                        / constraintsValues[current_row_ind][current_col_ind])
                    new_bi.append(current_v)
            ### Change to new ones
            print("before -----------")
            print(current_row_ind,current_col_ind)
            print(self.extraVars[0])
            print(self.extraVars[1])
            print(self.extraVars[2])
            print(bi)
            print(constraintsValues[0])
            print(constraintsValues[1])
            print(constraintsValues[2])
            self.extraVars[current_row_ind] = swap_var
            constraintsValues = new_constr_values
            bi = new_bi
            print("after-----------")
            print(self.extraVars[0])
            print(self.extraVars[1])
            print(self.extraVars[2])
            print(bi)
            print(constraintsValues[0])
            print(constraintsValues[1])
            print(constraintsValues[2])

    def _create_var_values_list(self, model, values):
        

    def _tableux(self, model, solution):
        """
        _tableux(model: Model, solution: Solution) -> list[list[float]]
            returns a tableux for the given model and solution
        """
        #TODO: this method should create an array (list of lists is fine, but you can cahnge it) 
        # representing the tableux for the given model and solution
        pass 

def _find_max_index(arr):
    best_val = arr[0]
    best_ind = 0
    for i in range(len(arr)):
        if arr[i] > best_val:
            best_ind = i
            best_val = arr[i]
    return best_ind

def _find_min_index(arr):
    best_val = arr[0]
    best_ind = 0
    for i in range(len(arr)):
        if arr[i] < best_val:
            best_ind = i
            best_val = arr[i]
    return best_ind