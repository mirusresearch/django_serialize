import unittest

from testproject.models import Parent

import django_serialize


class ModelToDictTests(unittest.TestCase):

    def test_it(self):
        pobj = Parent.objects.create(
            some_char_property='testing',
        )
        self.assertEqual(pobj.some_char_property, 'testing')
        res = django_serialize.model_to_dict(pobj)
        import pprint; pprint.pprint(res)
