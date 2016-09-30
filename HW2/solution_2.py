from numbers import Number


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

    def __str__(self):
        return str(self.constant_value)

    def evaluate(self):
        return self.constant_value

    def __add__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value + other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value - other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value - other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value * other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value * other)
        else:
            return NotImplemented

    def __pow__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value ** other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value ** other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value / other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value / other)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value // other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value // other)
        else:
            return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value % other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value % other)
        else:
            return NotImplemented

    def __lshift__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value << other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value << other)
        else:
            return NotImplemented

    def __rshift__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value >> other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value >> other)
        else:
            return NotImplemented

    def __and__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value & other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value & other)
        else:
            return NotImplemented

    def __xor__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value ^ other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value ^ other)
        else:
            return NotImplemented

    def __or__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value | other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value | other)
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value + other.constant_value)
        elif isinstance(other, Number):
            return Constant(self.constant_value + other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value - self.constant_value)
        elif isinstance(other, Number):
            return Constant(other - self.constant_value)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Constant):
            return Constant(self.constant_value * other.constant_value)
        elif isinstance(other, Number):
            return self.constant_value * other
        else:
            return NotImplemented

    def __rpow__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value ** self.constant_value)
        elif isinstance(other, Number):
            return Constant(other ** self.constant_value)
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value / self.constant_value)
        elif isinstance(other, Number):
            return Constant(other / self.constant_value)
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value // self.constant_value)
        elif isinstance(other, Number):
            return Constant(other // self.constant_value)
        else:
            return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value % self.constant_value)
        elif isinstance(other, Number):
            return Constant(other % self.constant_value)
        else:
            return NotImplemented

    def __rlshift__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value << self.constant_value)
        elif isinstance(other, Number):
            return Constant(other << self.constant_value)
        else:
            return NotImplemented

    def __rrshift__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value >> self.constant_value)
        elif isinstance(other, Number):
            return Constant(other >> self.constant_value)
        else:
            return NotImplemented

    def __rand__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value & self.constant_value)
        elif isinstance(other, Number):
            return Constant(other & self.constant_value)
        else:
            return NotImplemented

    def __rxor__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value ^ self.constant_value)
        elif isinstance(other, Number):
            return Constant(other ^ self.constant_value)
        else:
            return NotImplemented

    def __ror__(self, other):
        if isinstance(other, Constant):
            return Constant(other.constant_value | self.constant_value)
        elif isinstance(other, Number):
            return Constant(other | self.constant_value)
        else:
            return NotImplemented


class Variable:
    def __init__(self, var_name):
        self.var_name = var_name

    def evaluate(self, **kwargs):
        return kwargs[self.var_name]

    def __str__(self):
        return str(self.var_name)

    def __add__(self, other):
        plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
        if isinstance(other, Variable):
            return Expression((self, plus, other))
        elif isinstance(other, Constant):
            return Expression((self, plus, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, plus, other))
        else:
            return NotImplemented

    def __sub__(self, other):
        minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
        if isinstance(other, Variable):
            return Expression((self, minus, other))
        elif isinstance(other, Constant):
            return Expression((self, minus, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, minus, other))
        else:
            return NotImplemented

    def __mul__(self, other):
        times = create_operator('*', lambda lhs, rhs: lhs * rhs)
        if isinstance(other, Variable):
            return Expression((self, times, other))
        elif isinstance(other, Constant):
            return Expression((self, times, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, times, other))
        else:
            return NotImplemented

    def __pow__(self, other):
        power = create_operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Variable):
            return Expression((self, power, other))
        elif isinstance(other, Constant):
            return Expression((self, power, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, power, other))
        else:
            return NotImplemented

    def __truediv__(self, other):
        truediv = create_operator('/', lambda lhs, rhs: lhs / rhs)
        if isinstance(other, Variable):
            return Expression((self, truediv, other))
        elif isinstance(other, Constant):
            return Expression((self, truediv, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, truediv, other))
        else:
            return NotImplemented

    def __floordiv__(self, other):
        floordiv = create_operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Variable):
            return Expression((self, floordiv, other))
        elif isinstance(other, Constant):
            return Expression((self, floordiv, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, floordiv, other))
        else:
            return NotImplemented

    def __mod__(self, other):
        mod = create_operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Variable):
            return Expression((self, mod, other))
        elif isinstance(other, Constant):
            return Expression((self, mod, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, mod, other))
        else:
            return NotImplemented

    def __lshift__(self, other):
        lshift = create_operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Variable):
            return Expression((self, lshift, other))
        elif isinstance(other, Constant):
            return Expression((self, lshift, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, lshift, other))
        else:
            return NotImplemented

    def __rshift__(self, other):
        rshift = create_operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Variable):
            return Expression((self, rshift, other))
        elif isinstance(other, Constant):
            return Expression((self, rshift, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, rshift, other))
        else:
            return NotImplemented

    def __and__(self, other):
        logic_and = create_operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Variable):
            return Expression((self, logic_and, other))
        elif isinstance(other, Constant):
            return Expression((self, logic_and, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, logic_and, other))
        else:
            return NotImplemented

    def __xor__(self, other):
        logic_xor = create_operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Variable):
            return Expression((self, logic_xor, other))
        elif isinstance(other, Constant):
            return Expression((self, logic_xor, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, logic_xor, other))
        else:
            return NotImplemented

    def __or__(self, other):
        logic_or = create_operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Variable):
            return Expression((self, logic_or, other))
        elif isinstance(other, Constant):
            return Expression((self, logic_or, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, logic_or, other))
        else:
            return NotImplemented

    def __radd__(self, other):
        plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
        if isinstance(other, Variable):
            return Expression((self, plus, other))
        elif isinstance(other, Constant):
            return Expression((self, plus, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, plus, other))
        else:
            return NotImplemented

    def __rsub__(self, other):
        minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
        if isinstance(other, Variable):
            return Expression((other, minus, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, minus, self))
        elif isinstance(other, Number):
            return Expression((other, minus, self))
        else:
            return NotImplemented

    def __rmul__(self, other):
        times = create_operator('*', lambda lhs, rhs: lhs * rhs)
        if isinstance(other, Variable):
            return Expression((self, times, other))
        elif isinstance(other, Constant):
            return Expression((self, times, other.constant_value))
        elif isinstance(other, Number):
            return Expression((self, times, other))
        else:
            return NotImplemented

    def __rpow__(self, other):
        power = create_operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Variable):
            return Expression((other, power, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, power, self))
        elif isinstance(other, Number):
            return Expression((other, power, self))
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        truediv = create_operator('/', lambda lhs, rhs: lhs / rhs)
        if isinstance(other, Variable):
            return Expression((other, truediv, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, truediv, self))
        elif isinstance(other, Number):
            return Expression((other, truediv, self))
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        floordiv = create_operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Variable):
            return Expression((other, floordiv, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, floordiv, self))
        elif isinstance(other, Number):
            return Expression((other, floordiv, self))
        else:
            return NotImplemented

    def __rmod__(self, other):
        mod = create_operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Variable):
            return Expression((other, mod, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, mod, self))
        elif isinstance(other, Number):
            return Expression((other, mod, self))
        else:
            return NotImplemented

    def __rlshift__(self, other):
        lshift = create_operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Variable):
            return Expression((other, lshift, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, lshift, self))
        elif isinstance(other, Number):
            return Expression((other, lshift, self))
        else:
            return NotImplemented

    def __rrshift__(self, other):
        rshift = create_operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Variable):
            return Expression((other, rshift, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, rshift, self))
        elif isinstance(other, Number):
            return Expression((other, rshift, self))
        else:
            return NotImplemented

    def __rand__(self, other):
        logic_and = create_operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Variable):
            return Expression((other, logic_and, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, logic_and, self))
        elif isinstance(other, Number):
            return Expression((other, logic_and, self))
        else:
            return NotImplemented

    def __rxor__(self, other):
        logic_xor = create_operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Variable):
            return Expression((other, logic_xor, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, logic_xor, self))
        elif isinstance(other, Number):
            return Expression((other, logic_xor, self))
        else:
            return NotImplemented

    def __ror__(self, other):
        logic_or = create_operator('^', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Variable):
            return Expression((other, logic_or, self))
        elif isinstance(other, Constant):
            return Expression((other.constant_value, logic_or, self))
        elif isinstance(other, Number):
            return Expression((other, logic_or, self))
        else:
            return NotImplemented


class Operator:
    def __init__(self, op_symbol, op_function):
        self.op_symbol = op_symbol
        self.op_function = op_function

    def __str__(self):
        return str(self.op_symbol)


class Expression:
    def __init__(self, expression_structure):
        self.expression_structure = expression_structure

    def check_operand(self, operand, kwargs):
        if isinstance(operand, Variable):
            return kwargs[operand.var_name]
        elif isinstance(operand, Constant):
            return operand.constant_value
        else:
            return operand

    def min_evaluate(self, expression, kwargs):
        if isinstance(expression[0], Constant):
            if isinstance(expression[2], Constant):
                return expression[1].op_function(
                    expression[0].constant_value,
                    expression[2].constant_value)
            elif isinstance(expression[2], Variable):
                return expression[1].op_function(
                    expression[0].constant_value,
                    kwargs[expression[2].var_name])
            else:
                return expression[1].op_function(
                    expression[0].constant_value, expression[2])
        if isinstance(expression[0], Variable):
            if isinstance(expression[2], Variable):
                return expression[1].op_function(
                    kwargs[expression[0].var_name],
                    kwargs[expression[2].var_name])
            elif isinstance(expression[2], Constant):
                return expression[1].op_function(
                    kwargs[expression[0].var_name],
                    expression[2].constant_value)
            else:
                return expression[1].op_function(
                    kwargs[expression[0].var_name],
                    expression[2])
        if isinstance(expression[0], Number):
            if isinstance(expression[2], Constant):
                return expression[1].op_function(
                    expression[0], expression[2].constant_value)
            elif isinstance(expression[2], Variable):
                return expression[1].op_function(
                    expression[0], kwargs[expression[2].var_name])
            else:
                return expression[1].op_function(expression[0], expression[2])

    def evaluate_help(self, expression, variables):
        if isinstance(expression[0], tuple) and \
                isinstance(expression[2], tuple):
            return expression[1].op_function(
                self.evaluate_help(expression[0], variables),
                self.evaluate_help(expression[2], variables))
        if isinstance(expression[0], tuple):
            return expression[1].op_function(
                self.evaluate_help(expression[0], variables),
                self.check_operand(expression[2], variables))
        if isinstance(expression[2], tuple):
            return expression[1].op_function(
                self.check_operand(expression[0], variables),
                self.evaluate_help(expression[2], variables))
        else:
            return self.min_evaluate(expression, variables)

    def evaluate(self, **variables):
        sum = self.evaluate_help(self.expression_structure, variables)
        return sum

    def print_expression(self, expression):
        if isinstance(expression[0], tuple) and \
                isinstance(expression[2], tuple):
            return '(' + self.print_expression(expression[0]) + ')' + \
                ' ' + str(expression[1]) + ' ' + \
                '(' + self.print_expression(expression[2]) + ')'
        if isinstance(expression[0], tuple):
            return '(' + self.print_expression(expression[0]) + ')' + \
                ' ' + str(expression[1]) + ' ' + str(expression[2])
        if isinstance(expression[2], tuple):
            return str(expression[0]) + ' ' + str(expression[1]) + ' ' + \
                '(' + self.print_expression(expression[2]) + ')'
        else:
            return str(expression[0]) + ' ' + str(expression[1]) + ' ' + \
                str(expression[2])

    def find_var_names(self, expression):
        if isinstance(expression, tuple):
            res1 = self.find_var_names(expression[0])
            res2 = self.find_var_names(expression[2])
            res3 = []
            if(res1 is not None):
                res3 += res1
            if(res2 is not None):
                res3 += res2

            return res3
        elif isinstance(expression, Variable):
            return [expression.var_name]

    def __str__(self):
        return '(' + self.print_expression(self.expression_structure) + ')'

    def __add__(self, other):
        plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, plus,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure,
                               plus, other))

    def __sub__(self, other):
        minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, minus,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, minus,
                               other))

    def __mul__(self, other):
        times = create_operator('*', lambda lhs, rhs: lhs * rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, times,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, times,
                               other))

    def __pow__(self, other):
        power = create_operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, power,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, power,
                               other))

    def __truediv__(self, other):
        truediv = create_operator('/', lambda lhs, rhs: lhs / rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure,
                               truediv, other.expression_structure))
        else:
            return Expression((self.expression_structure,
                               truediv, other))

    def __floordiv__(self, other):
        floordiv = create_operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, floordiv,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, floordiv,
                               other))

    def __mod__(self, other):
        mod = create_operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, mod,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, mod,
                               other))

    def __lshift__(self, other):
        lshift = create_operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, lshift,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, lshift,
                               other))

    def __rshift__(self, other):
        rshift = create_operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, rshift,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, rshift,
                               other))

    def __and__(self, other):
        logic_and = create_operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, logic_and,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, logic_and,
                               other))

    def __xor__(self, other):
        logic_xor = create_operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, logic_xor,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, logic_xor,
                               other))

    def __or__(self, other):
        logic_xor = create_operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, logic_or,
                               other.expression_structure))
        else:
            return Expression((self.expression_structure, logic_or,
                               other))

    def __radd__(self, other):
        plus = create_operator('+', lambda lhs, rhs: lhs + rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, plus,
                               other.expression_structure))
        else:
            return Expression((other, plus, self.expression_structure))

    def __rsub__(self, other):
        minus = create_operator('-', lambda lhs, rhs: lhs - rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, minus,
                               self.expression_structure))
        else:
            return Expression((other, minus, self.expression_structure))

    def __rmul__(self, other):
        times = create_operator('*', lambda lhs, rhs: lhs * rhs)
        if isinstance(other, Expression):
            return Expression((self.expression_structure, times,
                               other.expression_structure))
        else:
            return Expression((other, times, self.expression_structure))

    def __rpow__(self, other):
        power = create_operator('**', lambda lhs, rhs: lhs ** rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, power,
                               self.expression_structure))
        else:
            return Expression((other, power, self.expression_structure))

    def __rtruediv__(self, other):
        truediv = create_operator('/', lambda lhs, rhs: lhs / rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, truediv,
                               self.expression_structure))
        else:
            return Expression((other, truediv, self.expression_structure))

    def __rfloordiv__(self, other):
        floordiv = create_operator('//', lambda lhs, rhs: lhs // rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, floordiv,
                               self.expression_structure))
        else:
            return Expression((other, floordiv, self.expression_structure))

    def __rmod__(self, other):
        mod = create_operator('%', lambda lhs, rhs: lhs % rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, mod,
                               self.expression_structure))
        else:
            return Expression((other, mod, self.expression_structure))

    def __rlshift__(self, other):
        lshift = create_operator('<<', lambda lhs, rhs: lhs << rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, lshift,
                               self.expression_structure))
        else:
            return Expression((other, lshift, self.expression_structure))

    def __rrshift__(self, other):
        rshift = create_operator('>>', lambda lhs, rhs: lhs >> rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, rshift,
                               self.expression_structure))
        else:
            return Expression((other, rshift, self.expression_structure))

    def __rand__(self, other):
        logic_and = create_operator('&', lambda lhs, rhs: lhs & rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, logic_and,
                               self.expression_structure))
        else:
            return Expression((other, logic_and, self.expression_structure))

    def __rxor__(self, other):
        logic_xor = create_operator('^', lambda lhs, rhs: lhs ^ rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, logic_xor,
                               self.expression_structure))
        else:
            return Expression((other, logic_xor, self.expression_structure))

    def __ror__(self, other):
        logic_xor = create_operator('|', lambda lhs, rhs: lhs | rhs)
        if isinstance(other, Expression):
            return Expression((other.expression_structure, logic_or,
                               self.expression_structure))
        else:
            return Expression((other, logic_or, self.expression_structure))


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return Operator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
