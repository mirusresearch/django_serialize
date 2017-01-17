import unittest

from testproject.models import Parent, ChildOneToOne, ChildManyToMany, ChildOneToMany

import django_serialize


class ModelToDictTests(unittest.TestCase):

    def setUp(self):
        ChildOneToOne.objects.all().delete()
        ChildManyToMany.objects.all().delete()
        ChildOneToMany.objects.all().delete()
        Parent.objects.all().delete()

    def test_simple(self):
        pobj = Parent.objects.create(
            some_char_property='testing',
        )
        self.assertEqual(pobj.some_char_property, 'testing')
        res = django_serialize.model_to_dict(pobj)
        self.assertEqual(res['some_char_property'], 'testing')
        # import pprint; pprint.pprint(res)

    def test_another(self):
        coto = ChildOneToOne.objects.create(
            some_int_property=1,
        )
        pobj = Parent.objects.create(
            some_char_property='testing',
            a_one_to_one_child=coto,
        )
        res = django_serialize.model_to_dict(pobj)
        self.assertEqual(res['a_one_to_one_child']['some_int_property'], 1)
        # import pprint; pprint.pprint(res)
