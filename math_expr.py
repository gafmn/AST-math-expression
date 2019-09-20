OPERATORS = ['<', '>', '=', '+', '-', '*', '(', ')']


class Expression:
    pass


class Lexer:

    def __init__(self, source):
        self.source = source
        self.ind = 0

    def next(self, source):
        while self.ind < len(source):
            if source[self.ind] in OPERATORS:
                self.ind = self.ind + 1
                return source[self.ind - 1]
            if source[self.ind].isdigit():
                number = ''
                while source[self.ind].isdigit():
                    number = number + source[self.ind]
                    if self.ind == len(source) - 1:
                        self.ind += 1
                        return number
                    self.ind = self.ind + 1

                return number
            self.ind = self.ind + 1
        return None


class Binary(Expression):

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Relation(Binary):
    pass


class Less(Relation):
    pass


class Greater(Relation):
    pass


class Equal(Relation):
    pass


class Term:
    pass


class Primary(Expression):
    pass


class Integer:

    def __init__(self, number):
        self.number = number


class Parenthesized:
    pass


class Parser:
    def __init__(self, source):
        self.source = source
        self.lexer = Lexer(source)

    def parse_integer(self):
        result = self.lexer.next(self.source)
        if result.isdigit():
            integer = Integer(result)
            return integer
        else:
            raise Exception("It is not a number")

    def parse_relation(self):
        left = self.parse_integer()
        token = self.lexer.next(self.source)
        if token is not None:
            right = self.parse_integer()
            if token == '<':
                result = Less(left, right)
            elif token == '>':
                result = Greater(left, right)
        else:
            return left
        return result


def main():
    source = '124<234'
    parser = Parser(source)
    print(parser.parse_relation())


if __name__ == '__main__':
    main()
