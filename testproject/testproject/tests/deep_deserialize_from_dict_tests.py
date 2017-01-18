import unittest

from testproject.models import Parent, ChildOneToOne, ChildManyToMany, ChildOneToMany

import django_serialize


class DeepDeserializeFromDictTests(unittest.TestCase):

    def big_test(self):
        dikt = {
            'some_char_property': 'what',
            # 'a_one_to_one_child': {
            #     'some_int_property': 3,
            # },
            'my_otm_children': [
                {'another_int_property': 2},
                {'another_int_property': 4},
            ],
        }
        model_obj = django_serialize.deep_deserialize_from_dict(dikt, Parent)
        self.assertEqual(model_obj.some_char_property, 'what')
        # self.assertEqual(model_obj.a_one_to_one_child.some_int_property, 3)
        self.assertEqual(model_obj.my_otm_children.count(), 2)
        otm_children = model_obj.my_otm_children.all()
        def filter_otm_children_by_prop_val(prop_val):
            return [otm_child for otm_child in otm_children if otm_child.another_int_property == prop_val]
        self.assertEqual(len(filter_otm_children_by_prop_val(2)), 1)
        self.assertEqual(len(filter_otm_children_by_prop_val(4)), 1)
