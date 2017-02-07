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

    def test_one_to_one(self):
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

    def test_one_to_many(self):
        pobj = Parent.objects.create(
            some_char_property='testing',
        )
        ChildOneToMany.objects.create(
            my_parent=pobj,
            another_int_property=2,
        )
        res = django_serialize.model_to_dict(pobj)
        # import pprint; pprint.pprint(res)
        self.assertEqual(len(res['my_otm_children']), 1)
        the_otm_child = res['my_otm_children'][0]
        self.assertEqual(the_otm_child['another_int_property'], 2)

    # F. Henard 1/17/17 - it appears that many to many isn't implemented
    # def test_many_to_many(self):
    #     cmtm = ChildManyToMany.objects.create(
    #         another_char_property='test2',
    #     )
    #     pobj = Parent.objects.create(
    #         some_char_property='testing',
    #     )
    #     pobj.a_many_to_many_child.add(cmtm)
    #     res = django_serialize.model_to_dict(pobj)
    #     import pprint; pprint.pprint(res)

    def test_foreign_key(self):
        pobj = Parent.objects.create(
            some_char_property='testing',
        )
        cotm = ChildOneToMany.objects.create(
            my_parent=pobj,
            another_int_property=2,
        )
        include_paths = {
            'my_parent': True,
            'another_int_property': True,
            'id': True,
        }
        res = django_serialize.model_to_dict(cotm, include_paths=include_paths)
        # import pprint; pprint.pprint(res)
        self.assertEqual(res['another_int_property'], 2)
        self.assertEqual(res['my_parent']['some_char_property'], 'testing')
