from django.db import models


class ChildOneToOne(models.Model):

    some_int_property = models.IntegerField(null=True, blank=True)


class ChildManyToMany(models.Model):

    another_char_property = models.CharField(max_length=50, null=True, blank=True)


class Parent(models.Model):

    some_char_property = models.CharField(max_length=50, null=True, blank=True)
    a_one_to_one_child = models.OneToOneField(ChildOneToOne, null=True, blank=True)
    a_many_to_many_child = models.ManyToManyField(ChildManyToMany)


class ChildOneToMany(models.Model):

    my_parent = models.ForeignKey(Parent)
