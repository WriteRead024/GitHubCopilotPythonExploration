
# adapted from
# https://docs.python.org/3/library/unittest.html
# local Python version 3.12.1
# Feb. 21, 2022
# Rich W.

import unittest

# class RenamedTestStringMethods(): # also works
class RenamedTestStringMethods:

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()