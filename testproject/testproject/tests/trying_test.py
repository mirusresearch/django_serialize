import unittest

from testproject.models import Parent


class TryingTest(unittest.TestCase):

    def test_it(self):
        pobj = Parent.objects.create(
            some_char_property='testing',
        )
        self.assertEqual(pobj.some_char_property, 'testing')
