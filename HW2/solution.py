class Constant:
    def __init__(self, constant_value):
        self.constant_value = constant_value

    def __getattr__(self, constant_value):
        return constant_value

    def __int__(self):
        return int(self.constant_value)

    def __float__(self):
        return float(self.constant_value)

    def __complex__(self):
        return complex(self.constant_value)

    def __add__(self, other):
        return self.constant_value + other.constant_value

    def __sub__(self, other):
        return self.constant_value - other.constant_value

    def __mul__(self, other):
        return self.constant_value * other.constant_value

    def __truediv__(self, other):
        return self.constant_value / other.constant_value

    def __floordiv__(self, other):
        return self.constant_value // other.constant_value

    def __mod__(self, other):
        return self.constant_value % other.constant_value

    def __lshift__(self, other):
        return self.constant_value << other.constant_value

    def __rshift__(self, other):
        return self.constant_value >> other.constant_value

    def __and__(self, other):
        return self.constant_value & other.constant_value

    def __xor__(self, other):
        return self.constant_value ^ other.constant_value

    def __or__(self, other):
        return self.constant_value | other.constant_value


class Variable(Constant):
    def __init__(self, var_name):
        self.var_name = var_name

    def __getattr__(self, var_name):
        return var_name

    def __getattr__(self, value):
        return value

    def __setattr__(self, var_name, value):
        return object.__setattr__(self, var_name, value)


class Operator:
    def __init__(self, op_symbol, op_function):
        self.op_symbol = op_symbol
        self.op_function = op_function

    def __str__(self):
        return str(self.op_symbol)


class Expression:
    def __init__(self, expression_structure):
        self.expression_structure = expression_structure

    def evaluate(self, **variables):
        for i in range(len(self.expression_structure)):
            var = self.expression_structure
            if isinstance(var[i], Variable):
                for key in variables:
                    if key == var[i].var_name:
                        var[i].value = variables[key]

        def evaluate_help(expression):
            sum = 0
            for i in range(len(expression)):
                var = expression
                if isinstance(var[i], Operator):
                    if isinstance(var[i - 1], tuple):
                        print(type(evaluate_help(var[i - 1])))
                    elif isinstance(var[i + 1], tuple):
                        print(type(evaluate_help(var[i - 1])))
                    elif isinstance(var[i - 1], Variable) and isinstance(var[i + 1], Variable):
                        sum += var[i].op_function(var[i -
                                                      1].value, var[i + 1].value)
                    elif isinstance(var[i - 1], Variable) and isinstance(var[i + 1], Constant):
                        sum += var[i].op_function(var[i -
                                                      1].value, var[i + 1].constant_value)
                    elif isinstance(var[i - 1], Constant) and isinstance(var[i + 1], Variable):
                        sum += var[i].op_function(var[i -
                                                      1].constant_value, var[i + 1].value)
                    elif isinstance(var[i - 1], Constant) and isinstance(var[i + 1], Constant):
                        sum += var[i].op_function(
                            var[i - 1].constant_value, var[i + 1].constant_value)
            return sum

        sum = evaluate_help(self.expression_structure)

        return sum

        """
        for i in range(len(self.expression_structure)):
            var = self.expression_structure
            if isinstance(var[i], tuple):
                print ("na bati")
                return evaluate(var[i])
            if isinstance(var[i], Operator):
                if isinstance(var[i-1], Constant) and isinstance(var[i+1], Constant):
                    print (var[i].op_function(var[i-1], var[i+1]))
            else:
                print("Kote")
        return sum
        """


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return Operator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)


"""
six = create_constant(6)
fifteen = create_constant(15)

seven_five = create_constant(7.5)

x = create_variable('x')
y = create_variable('y')

plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
times = create_operator('*', lambda lhs, rhs: lhs * rhs)

print (six + fifteen)
print (six - fifteen)
print (six * fifteen)
print (fifteen / six)


print (seven_five + six)
print (seven_five - six)
print (seven_five * six)
print (seven_five / six)

print (seven_five % six)



print (int(fifteen) + 3)

print (complex(seven_five))

print (3 == 3.0)

#print (3 + x)(x=3)
"""


plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
times = create_operator('*', lambda lhs, rhs: lhs * rhs)

six = create_constant(6)
nine = create_constant(9)
expression = create_expression((six, times, nine))

expression2 = create_expression((six, times, ((six, minus, nine))))
print(expression.evaluate())
print(expression2.evaluate)


#plus = create_operator('+', lambda lhs, rhs: lhs + rhs)

