import random
import unittest

import pytransaction.errors
from pytransaction import Transaction

n0 = random.random()


class TesteClass(Transaction):
    def __init__(self, value=n0):
        self.test = value
        super(TesteClass, self).__init__()


class TestException(Exception):
    pass


class TestPyTransaction(unittest.TestCase):

    def test_01(self):
        t = TesteClass()
        self.assertEqual(t.test, n0)

    def test_02(self):
        n = random.random()
        t = TesteClass()
        t.test = n
        self.assertEqual(t.test, n)

    def test_03(self):
        n = random.random()
        t = TesteClass()
        t.test = n
        t.commit()

    def test_04(self):
        n = random.random()
        t = TesteClass()
        t.test = n
        t.begin()
        self.assertEqual(t.test, n)
        t.commit()
        self.assertEqual(t.test, n)

    def test_05(self):
        n1 = random.random()
        t = TesteClass()
        t.test = n1
        t.begin()
        n2 = random.random()
        t.test = n2
        self.assertEqual(t.test, n2)
        t.rollback()
        self.assertEqual(t.test, n1)

    def test_06(self):
        n1 = random.random()
        t = TesteClass()
        t.test = n1
        t.begin()
        n2 = random.random()
        t.test = n2
        t.commit()
        self.assertEqual(t.test, n2)

    def test_07(self):
        n1 = random.random()
        t = TesteClass()
        t.test = n1
        t.begin()
        n2 = random.random()
        t.test = n2
        t.commit()
        t.rollback()
        self.assertEqual(t.test, n2)

    def test_08(self):
        n1 = random.random()
        t = TesteClass()
        t.test = n1
        t.begin()
        n2 = random.random()
        t.test = n2
        t.begin()
        n3 = random.random()
        t.test = n3
        t.rollback()
        self.assertEqual(t.test, n2)
        t.rollback()
        self.assertEqual(t.test, n1)

    def test_09(self):
        n1 = random.random()
        t = TesteClass()
        t.test = n1
        t.begin()
        n2 = random.random()
        t.test = n2
        t.begin()
        n3 = random.random()
        t.test = n3
        t.rollback()
        self.assertEqual(t.test, n2)
        t.commit()
        self.assertEqual(t.test, n2)
        t.rollback()
        self.assertEqual(t.test, n2)

    def test_10(self):
        t = TesteClass()
        with self.assertRaises(pytransaction.errors.CommitFirstError):
            t.rollback(ignore_no_commit=False)

    def test_11(self):
        t = TesteClass()
        n1 = random.random()
        n2 = random.random()

        with t:
            t.test = n1
            with t:
                t.test = n2
            self.assertEqual(t.test, n2)
        self.assertEqual(t.test, n2)

    def test_12(self):
        t = TesteClass()
        n1 = random.random()
        n2 = random.random()
        n3 = random.random()

        with t:
            t.test = n1
            self.assertEqual(t.test, n1)
            with t:
                t.test = n2
            self.assertEqual(t.test, n2)
            with self.assertRaises(TestException):
                with t:
                    t.test = n3
                    raise TestException
            self.assertEqual(t.test, n2)
        self.assertEqual(t.test, n2)

    def test_13(self):
        t = TesteClass()
        n1 = random.random()
        n2 = random.random()
        with self.assertRaises(TestException):
            with t:
                t.test = n1
                self.assertEqual(t.test, n1)
                with t:
                    t.test = n2
                self.assertEqual(t.test, n2)
                raise TestException("Test exception")
        self.assertEqual(t.test, n2)


if __name__ == '__main__':
    unittest.main()
