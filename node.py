import classes


class Symbol:
    def __init__(self, _type, identifier, temp_register):
        self.type = _type
        self.identifier = identifier
        self.temp_register = temp_register


class SymbolsTable:
    def __init__(self):
        self.symbols = {}


class Scope:
    def __init__(self):
        self.symbols_tables = []

    def check_repeat_declaration(self, identifier):
        if len(self.symbols_tables) > 0:
            if str(identifier) in self.symbols_tables[-1].keys():
                return True
            return False
        return False

    def get_symbol(self, identifier):
        if len(self.symbols_tables) > 0:
            for i in range(len(self.symbols_tables) - 1, -1, -1):
                if str(identifier) in self.symbols_tables[i].symbols.keys():
                    return self.symbols_tables[i].symbols[str(identifier)]
        return None

    def bind_temp_register_to_symbol(self, identifier, temp_register):
        if len(self.symbols_tables) > 0:
            for i in range(len(self.symbols_tables) - 1, -1, -1):
                if str(identifier) in self.symbols_tables[i].symbols.keys():
                    self.symbols_tables[i].symbols[str(identifier)].temp_register = temp_register
                    return True
            return False
        return False


class Node:
    def __init__(self, ast):
        self.ast = ast
        self.code3d = "main:\n"
        self.counter_register_temp = 1
        self.counter_label_temp = 1
        self.functions = {}
        self.scopes = []

    def get_symbol(self, identifier):
        if len(self.scopes) > 0:
            symbol = self.scopes[-1].get_symbol(identifier)
            if symbol:
                return symbol
            symbol = self.scopes[0].get_symbol(identifier)
            if symbol:
                return symbol
            return None
        return None

    def generate_code_main(self):
        self.code3d += "begin:\n"
        main = self.functions["main"]
        self.gen_code_instructions(main.body)
        self.code3d += "end\n\n"

    def gen_code_instructions(self, instructions):
        if instructions:
            for instruction in instructions:
                if isinstance(instruction, classes.Assignment):
                    self.gen_code_assignment(instruction)

    def gen_code_assignment(self, instruction):
        if isinstance(instruction, classes.AssignmentNormal):
            self.gen_code_assignment_normal(instruction)

    def gen_code_assignment_normal(self, instruction):
        symbol = self.get_symbol(instruction.identifier)
        if symbol:
            if instruction.indices:
                register = symbol.temp_register
                for access in instruction.indices:
                    temp_register_expression = self.get_expression(access)
                    # todo
                    # 假如访问的是数组元素
            else:
                temp_register_expression = self.get_expression(instruction.expression)
                if temp_register_expression:
                    register = symbol.temp_register
                    # todo
                    # 为变量绑定一个临时标识符
                    if len(self.scopes) > 0:
                        if self.scopes[-1].bind_temp_register_to_symbol(symbol.identifier, register) or \
                                self.scopes[0].bind_temp_register_to_symbol(symbol.identifier, register):
                            self.gen_composite_code(instruction, register, temp_register_expression)

                    self.code3d += f"{register} = {temp_register_expression}\n"

    def gen_composite_code(self, instruction, register, temp_register_expression):
        if instruction.compuesto == '=':
            self.code3d += register + " = " + temp_register_expression + '\n'
        elif instruction.compuesto == '+':
            self.code3d += register + " = " + register + " + " + temp_register_expression + '\n'
        elif instruction.compuesto == '-':
            self.code3d += register + " = " + register + " - " + temp_register_expression + '\n'
        elif instruction.compuesto == '*':
            self.code3d += register + " = " + register + " * " + temp_register_expression + '\n'
        elif instruction.compuesto == '/':
            self.code3d += register + " = " + register + " / " + temp_register_expression + '\n'
        elif instruction.compuesto == '%':
            self.code3d += register + " = " + register + " % " + temp_register_expression + '\n'
        elif instruction.compuesto == '<<':
            self.code3d += register + " = " + register + '<<' + temp_register_expression + '\n'
        elif instruction.compuesto == '>>':
            self.code3d += register + " = " + register + '>>' + temp_register_expression + '\n'
        elif instruction.compuesto == '&':
            self.code3d += register + " = " + register + " & " + temp_register_expression + '\n'
        elif instruction.compuesto == '^':
            self.code3d += register + " = " + register + " ^ " + temp_register_expression + '\n'
        elif instruction.compuesto == '|':
            self.code3d += register + " = " + register + " | " + temp_register_expression + '\n'

    def new_temp_register(self):
        temp_register = 't' + str(self.counter_register_temp)
        self.counter_register_temp += 1
        return temp_register

    def new_temp_label(self):
        temp_label = 'L' + str(self.counter_label_temp)
        self.counter_label_temp += 1
        return temp_label

    def get_expression(self, expression):
        if isinstance(expression, classes.ExpressionArithmetic):
            return self.get_arithmetic_expression(expression)
        if isinstance(expression, classes.ExpressionRelational):
            return self.get_relational_expression(expression)
        if isinstance(expression, classes.ExpressionLogical):
            return self.get_logical_expression(expression)
        if isinstance(expression, classes.ExpressionBit):
            return self.get_bit_expression(expression)
        if isinstance(expression, classes.ExpressionUnary):
            return self.get_unary_expression(expression)

    def get_arithmetic_expression(self, expression):
        """
        生成二元算术表达式的三地址码，并返回存储当前表达式值的临时变量标识符
        :param expression:
        :return:
        """
        first = self.get_expression(expression.first)
        second = self.get_expression(expression.second)
        if first and second:
            register = self.new_temp_register()
            self.code3d += f"{register} = {first} {expression.operator} {second}\n"
            return register
        return None

    def get_relational_expression(self, expression):
        """
        生成关系表达式的三地址码，并返回存储当前表达式值的临时变量标识符
        :param expression:
        :return:
        """
        first = self.get_expression(expression.first)
        second = self.get_expression(expression.second)
        if first and second:
            register = self.new_temp_register()
            self.code3d += f"{register} = {first} {expression.operator} {second}\n"
            return register
        return None

    def get_logical_expression(self, expression):
        """
        生成逻辑表达式的三地址码，并返回存储当前表达式值的临时变量标识符
        :param expression:
        :return:
        """
        first = self.get_expression(expression.first)
        second = self.get_expression(expression.second)
        if first and second:
            register = self.new_temp_register()
            self.code3d += f"{register} = {first} {expression.operator} {second}\n"
            return register
        return None

    def get_bit_expression(self, expression):
        """
        生成位运算表达式的三地址码，并返回存储当前表达式值的临时变量标识符
        :param expression:
        :return:
        """
        first = self.get_expression(expression.first)
        second = self.get_expression(expression.second)
        if first and second:
            register = self.new_temp_register()
            self.code3d += f"{register} = {first} {expression.operator} {second}\n"
            return register
        return None

    def get_unary_expression(self, expression):
        """
        生成一元表达式的三地址码，并返回存储当前表达式值的临时变量标识符
        :param expression:
        :return:
        """
        operand = self.get_expression(expression.operand)
        if operand:
            register = self.new_temp_register()
            self.code3d += f"{register} = {expression.operator}{expression.operand}\n"
            return register
        return None

    # todo
    def get_if_expression(self, expression):
        """
        生成判断表达式的三地址码
        :param expression:
        :return:
        """
        return None
