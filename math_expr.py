OPERATORS = ['<', '>', '=', '+', '-', '*', '(', ')']


class Expression:
    pass


class Lexer:

    def __init__(self, source):
        self.source = source
        self.ind = 0
        self.token = None

    def next(self):
        symbol = ''

        while self.ind < len(self.source):
            if self.source[self.ind] in OPERATORS:
                symbol = self.source[self.ind]
                self.ind = self.ind + 1
                self.token = symbol
                return self.token

            elif self.source[self.ind].isdigit():
                number = ''
                while self.source[self.ind].isdigit():
                    number = number + self.source[self.ind]
                    if self.ind == len(self.source) - 1:
                        self.ind += 1
                        break
                    self.ind = self.ind + 1
                self.token = number
                return self.token

            self.ind = self.ind + 1

        return None

    def current(self):
        return self.token


class Binary(Expression):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Relation(Binary):
    pass


class Less(Relation):
    def calculate(self):
        print('Less calculate')
        if self.left.calculate() < self.right.calculate():
            return 1
        else:
            return 0


class Greater(Relation):
    def calculate(self):
        print('Greater calculate')
        if self.left.calculate() > self.right.calculate():
            return 1
        else:
            return 0


class Equal(Relation):
    def calculate(self):
        print('Equal calculate')
        if self.left.calculate() == self.right.calculate():
            return 1
        else:
            return 0


class Term(Expression):

    def __init__(self):
        self.factors = []

    def add_factor(self, sign, factor):
        self.factors.append((sign, factor))

    def calculate(self):
        print('Term calculate')
        result = 0
        for item in self.factors:
            result += item[0] * item[1].calculate()
        return result


class Factor(Expression):

    def __init__(self):
        self.primaries = []

    def add_primary(self, primary):
        self.primaries.append(primary)

    def calculate(self):
        print('Factor calculate')
        result = 1
        for item in self.primaries:
            result *= item.calculate()
        return result


class Primary(Expression):
    pass


class Integer(Primary):

    def __init__(self, number):
        self.number = number

    def calculate(self):
        print('Integer calculate')
        return int(self.number)


class Parenthesized(Primary):
    def __init__(self, expression):
        self.expression = expression

    def calculate(self):
        print('Parenthesized calculate')
        return self.expression.calculate()


class Parser:
    def __init__(self, source):
        self.source = source
        self.lexer = Lexer(source)

    def parse(self):
        return self.parse_relation()

    def parse_relation(self):
        left = self.parse_term()
        token = self.lexer.current()
        if token is not None:
            if token == '<':
                right = self.parse_term()
                result = Less(left, right)
            elif token == '>':
                right = self.parse_term()
                result = Greater(left, right)
            elif token == '=':
                right = self.parse_term()
                result = Equal(left, right)
            else:
                return left
            return result
        return left

    def parse_term(self):
        term = Term()
        factor = self.parse_factor()
        term.add_factor(1, factor)

        is_end = False
        while not is_end:
            token = self.lexer.current()
            if token == '+':
                factor = self.parse_factor()
                term.add_factor(1, factor)
            elif token == '-':
                factor = self.parse_factor()
                term.add_factor(-1, factor)
            else:
                is_end = True

        return term

    def parse_factor(self):
        factor = Factor()
        primary = self.parse_primary()
        factor.add_primary(primary)
        is_end = False
        while not is_end:
            token = self.lexer.next()
            if token == '*':
                primary = self.parse_primary()
                factor.add_primary(primary)
            else:
                is_end = True
        return factor

    def parse_primary(self):
        token = self.lexer.next()

        if token is not None:
            if token.isdigit():
                result = Integer(token)
                return result
            elif token == '(':
                result = self.parse_relation()
                if self.lexer.current() == ')':
                    return Parenthesized(result)
                else:
                    raise Exception('This is no close bracket')
            else:
                raise Exception("Invalid primary")
        else:
            raise Exception("No primary to parse")


def main():
    source = '(10000*1000 < 2) * 228 - 1'
    parser = Parser(source)

    tree = parser.parse()
    result = tree.calculate()
    print(f"Result: {result}")


if __name__ == '__main__':
    main()
