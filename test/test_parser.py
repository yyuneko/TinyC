import unittest
from lexer import Lexer
from parser import Parser
import os


class TestParser(unittest.TestCase):
    def test_build(self):
        parser = Parser(Lexer(os.path.realpath("./test_lexer.in")))
        parser.build()
        # print(parser.s)


if __name__ == '__main__':
    unittest.main()
