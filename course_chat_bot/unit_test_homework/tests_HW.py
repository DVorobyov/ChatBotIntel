import unittest
from course_chat_bot.unit_test_homework.calculator_test_homework\
    import Calculator


class TestCalculator(unittest.TestCase):

    def test_sub(self):
        self.assertEqual(Calculator.sub(10, 1), 9)

    def test_div(self):
        self.assertEqual(Calculator.div(1, 2), 1/2)

    def test_add(self):
        self.assertNotEqual(Calculator.add(1, 2), 2)

    def test_check_operator_0(self):
        self.assertFalse(Calculator.check_operator_int('&'))

    def test_check_operator_1(self):
        self.assertTrue(Calculator.check_operator_int('/'))

    def test_calculation_str_0(self):
        Mystr = 'Hello'
        self.assertIs(Mystr, Calculator.add(Mystr, ''))

    def test_add_str(self):
        Mystr = 'Hello my'
        self.assertNotIn(Mystr, Calculator.calculate(Mystr, ' world', '-'))

    def test_calcalation_int_1(self):
        self.assertIsNot([2], [Calculator.add(1, 1)])

    def test_calculation_int_div(self):
        self.assertEqual(Calculator.calculate_int(4, 2, '/'), 2)

    def test_calculation_sub(self):
        self.assertEqual(Calculator.calculate_int(2, 1, '-'), 1)

    def test_div_except(self):
        self.assertEqual(Calculator.div(1, 0), 0)

    def test_calculate_none(self):
        self.assertIsNotNone(Calculator.calculate_int(1, 2, '+'))

    def test_operator_tuple_0(self):
        self.assertIn('+', Calculator.operator_tuple_int)

    def test_calculation_0(self):
        self.assertIsNone(Calculator.calculate_int(2, 3, '&'))

    def test_calculation_str_1(self):
        self.assertIsInstance(Calculator.calculate_int(1, 2, '+'), int)

    def test_calculation_str_2(self):
        self.assertNotIsInstance(Calculator.calculate('2', '3', '+'), int)

    def test_calculation_str_3(self):
        self.assertWarns(Warning, Calculator.calculate,
                         '', 'warn me please', '+')

    def test_check_operator_str(self):
        pass


if __name__ == '__main__':
    unittest.main()
