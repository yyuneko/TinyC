import unittest
from lexer import Lexer
import os


class TestLexer(unittest.TestCase):
    def test_get_tokens(self):
        lexer = Lexer(os.path.realpath("./test_lexer.in"))
        # self.assertEqual()
        tokens = lexer.get_tokens()
        # for token in tokens:
        #     print(token)


if __name__ == '__main__':
    unittest.main()
