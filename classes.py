class Expression:
    pass


class ExpressionArithmetic(Expression):
    def __init__(self, first, operator, second):
        self.first = first
        self.operator = operator
        self.second = second


class ExpressionRelational(Expression):
    def __init__(self, first, operator, second):
        self.first = first
        self.operator = operator
        self.second = second


class ExpressionLogical(Expression):
    def __init__(self, first, operator, second):
        self.first = first
        self.operator = operator
        self.second = second


class ExpressionBit(Expression):
    def __init__(self, first, operator, second):
        self.first = first
        self.operator = operator
        self.second = second


class ExpressionUnary(Expression):
    def __init__(self, operand, operator):
        self.operand = operand
        self.operator = operator


class ExpressionIf(Expression):
    def __init__(self, condition, ):
        pass


class Assignment:
    pass


class AssignmentNormal(Assignment):
    def __init__(self, identifier, indices,expression):
        self.identifier = identifier
        self.indices = indices
        self.expression=expression


class Function:
    def __init__(self):
        pass

class Identifier:
    def __init__(self,value,shape=None):
        self.value=value
        self.shape=shape

class Num:
    def __init__(self,value):
        self.value = value

class Real:
    def __init__(self,value):
        self.value = value
class ArrayAccess:
    def __init__(self,identifier, indices):