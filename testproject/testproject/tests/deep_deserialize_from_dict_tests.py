import unittest

from testproject.models import Parent, ChildOneToOne, ChildManyToMany, ChildOneToMany

import django_serialize


class DeepDeserializeFromDictTests(unittest.TestCase):

    def setUp(self):
        ChildOneToOne.objects.all().delete()
        ChildManyToMany.objects.all().delete()
        ChildOneToMany.objects.all().delete()
        Parent.objects.all().delete()

    def test_new(self):
        dikt = {
            'some_char_property': 'what',
            'a_one_to_one_child': {
                'some_int_property': 3,
            },
            'my_otm_children': [
                {'another_int_property': 2},
                {'another_int_property': 4},
            ],
        }
        model_obj = django_serialize.deep_deserialize_from_dict(dikt, Parent)
        self.assertEqual(model_obj.some_char_property, 'what')
        self.assertEqual(model_obj.a_one_to_one_child.some_int_property, 3)
        self.assertEqual(model_obj.my_otm_children.count(), 2)
        otm_children = model_obj.my_otm_children.all()
        self.assertEqual(len(filter_otm_children_by_prop_val(otm_children, 2)), 1)
        self.assertEqual(len(filter_otm_children_by_prop_val(otm_children, 4)), 1)

    def test_existing(self):
        coto = ChildOneToOne.objects.create(
            some_int_property=2,
        )
        pobj = Parent.objects.create(
            some_char_property='what',
            a_one_to_one_child=coto,
        )
        cotm1 = ChildOneToMany.objects.create(
            my_parent=pobj,
            another_int_property=2,
        )
        cotm2 = ChildOneToMany.objects.create(
            my_parent=pobj,
            another_int_property=4,
        )
        dikt = {
            'id': pobj.id,
            'some_char_property': 'nothing',
            'a_one_to_one_child': {
                'id': coto.id,
                'some_int_property': 4,
            },
            'my_otm_children': [
                {
                    'id': cotm1.id,
                    'another_int_property': 3,
                },
                {
                    'id': cotm2.id,
                    'another_int_property': 5,
                },
            ]
        }
        model_obj = django_serialize.deep_deserialize_from_dict(dikt, Parent)
        self.assertEqual(model_obj.some_char_property, 'nothing')
        self.assertEqual(model_obj.a_one_to_one_child.some_int_property, 4)
        self.assertEqual(model_obj.my_otm_children.count(), 2)
        otm_children = model_obj.my_otm_children.all()
        self.assertEqual(len(filter_otm_children_by_prop_val(otm_children, 3)), 1)
        self.assertEqual(len(filter_otm_children_by_prop_val(otm_children, 5)), 1)


def filter_otm_children_by_prop_val(otm_children, prop_val):
    return [otm_child for otm_child in otm_children if otm_child.another_int_property == prop_val]
