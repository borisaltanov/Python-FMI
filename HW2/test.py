import unittest

import solution_2 as solution


class Test_every_operator(unittest.TestCase):
    def test_every_operator(self):
        a = solution.create_variable('a')
        b = solution.create_variable('b')
        x = ((((5 // b) << (5 % b)) ** b) >> (((5 | b) - (5 & b)) ^ b))
        y = ((((a // 3) << (a % 3)) ** 3) >> (((a | 3) - (a & 3)) ^ 3))
        z = ((((a // b) << (a % b)) ** b) >> (((a | b) - (a & b)) ^ b))
        self.assertEqual(x.evaluate(b=3), 2)
        self.assertEqual(y.evaluate(a=5), 2)
        self.assertEqual(z.evaluate(a=5, b=3), 2)

if __name__ == '__main__':
    unittest.main()
