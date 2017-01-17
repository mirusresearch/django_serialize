import unittest

from testproject.models import Parent


class TryingTest(unittest.TestCase):

    def test_it(self):
        pobj = Parent.objects.create(
            some_char_property='testing',
        )
        # import os, inspect
        # currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # parentdir = os.path.dirname(currentdir)
        import django_serialize
        res = django_serialize.model_to_dict(pobj)
        import pprint; pprint.pprint(res)
        # import pprint, sys; pprint.pprint(sys.path)
        # import pdb; pdb.set_trace()
        self.assertEqual(pobj.some_char_property, 'testing')
