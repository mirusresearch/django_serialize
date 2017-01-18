import logging

logger = logging.getLogger(__name__)


def model_to_dict(model_obj, deep=True, include_paths={}, path=[], type_converters={}):
    import decimal
    import datetime
    import copy
    # import pprint
    # from mirus.django import converters
    # from mirus import utils as mirus_utils
    if not model_obj:
        return None
    RELATED_OBJ_TYPE = "django.db.models.related.RelatedObject"
    MANY_TO_ONE_REL_TYPE = 'django.db.models.fields.related.ManyToOneRel'
    RELATED_TYPES = [RELATED_OBJ_TYPE, MANY_TO_ONE_REL_TYPE]
    RELATED_MGR_TYPE = "django.db.models.fields.related.RelatedManager"
    ONE_TO_ONE_TYPE = "django.db.models.fields.related.OneToOneField"
    # model_as_dict = copy.deepcopy(model_obj.__dict__)  # F. Henard 10/29/15 - deepcopy causing a problem in django 1.8.
    # Pretty sure we don't need to deepcopy because we are diving into the model through _meta.get_all_field_names()
    model_as_dict = copy.copy(model_obj.__dict__)
    model_fieldnames = model_obj._meta.get_all_field_names()
    def should_exclude_field(_fieldname):
        return fieldname not in model_fieldnames or \
            include_paths and \
            ((isinstance(include_paths, list) and _fieldname not in include_paths) or \
             (isinstance(include_paths, dict) and _fieldname not in include_paths.keys()))
    exclusion_fieldname_list = [fieldname for fieldname in model_as_dict.keys() if should_exclude_field(fieldname)]
    model_as_dict = exclude_from_dict(model_as_dict, exclusion_fieldname_list)
    # logger.debug(pprint.pformat({
    #     'path': path,
    #     'include_paths': include_paths,
    #     'model_as_dict': model_as_dict,
    # }))
    for field_name in model_fieldnames:
        curr_path = path + [field_name]
        next_include_paths = {}
        if include_paths:
            can_recurse = False
            if isinstance(include_paths, dict):
                next_include_paths = include_paths.get(field_name)
                can_recurse = bool(next_include_paths)
            elif isinstance(include_paths, list):
                next_include_paths = True
                can_recurse = field_name in include_paths
            elif isinstance(include_paths, bool):
                can_recurse = False
            else:
                raise Exception("unrecognized include path type of '%s'" % type(include_paths))
            if not can_recurse:
                continue
        field = model_obj._meta.get_field_by_name(field_name)[0]
        try:
            field_value = model_obj.__getattribute__(field_name)
        except AttributeError:
            continue
        # logger.debug(pprint.pformat({
        #     'path': curr_path,
        #     'field_type': class_fullname(type(field)),
        #     'include_paths': include_paths,
        #     'next_include_paths': next_include_paths,
        # }))
        # logger.debug("path = %s; field type = %s" % (curr_path, class_fullname(type(field))))
        # if deep and class_fullname(type(field)) == RELATED_OBJ_TYPE and class_fullname(type(field_value)) == RELATED_MGR_TYPE:
        if deep and class_fullname(type(field)) in RELATED_TYPES and class_fullname(type(field_value)) == RELATED_MGR_TYPE:
            model_as_dict[field_name] = [
                model_to_dict(
                    child,
                    path=curr_path,
                    include_paths=next_include_paths,
                ) for child in field_value.all()]
        elif deep and class_fullname(type(field)) == ONE_TO_ONE_TYPE and not isinstance(field_value, int):
            # F. Henard 1/26/15 - Checking for int because in django 1.7 the id of the one-to-one relation is of type OneToOneField
            model_as_dict[field_name] = model_to_dict(
                field_value,
                path=curr_path,
                include_paths=next_include_paths,
            )
        elif isinstance(field_value, decimal.Decimal):
            model_as_dict[field_name] = float(field_value)
        elif type(field_value) == datetime.datetime:
            datetime_converter = type_converters.get('datetime.datetime')
            model_as_dict[field_name] = datetime_converter(field_value) if datetime_converter else field_value.isoformat()
    return model_as_dict


# # def model_to_dict(model_obj, deep=True, date_format=STD_DATE_FORMAT):
# def model_to_dict(model_obj, deep=True):
#     import decimal
#     import datetime
#     import copy
#     from mirus import mirus_utils
#     if not model_obj:
#         return None
#     RELATED_OBJ_TYPE = "django.db.models.related.RelatedObject"
#     RELATED_MGR_TYPE = "django.db.models.fields.related.RelatedManager"
#     ONE_TO_ONE_TYPE = "django.db.models.fields.related.OneToOneField"
#     # model_as_dict = copy.deepcopy(model_obj.__dict__)  # F. Henard 10/29/15 - deepcopy causing a problem in django 1.8.
#     # Pretty sure we don't need to deepcopy because we are diving into the model through _meta.get_all_field_names()
#     model_as_dict = copy.copy(model_obj.__dict__)
#     model_fieldnames = model_obj._meta.get_all_field_names()
#     exclusion_fieldname_list = [fieldname for fieldname in model_as_dict.keys() if fieldname not in model_fieldnames]
#     model_as_dict = exclude_from_dict(model_as_dict, exclusion_fieldname_list)
#     for field_name in model_fieldnames:
#         field = model_obj._meta.get_field_by_name(field_name)[0]
#         try:
#             field_value = model_obj.__getattribute__(field_name)
#         except AttributeError:
#             continue
#         if deep and class_fullname(type(field)) == RELATED_OBJ_TYPE and class_fullname(type(field_value)) == RELATED_MGR_TYPE:
#             model_as_dict[field_name] = [model_to_dict(child) for child in field_value.all()]
#         elif deep and class_fullname(type(field)) == ONE_TO_ONE_TYPE and not isinstance(field_value, int):
#             # F. Henard 1/26/15 - Checking for int because in django 1.7 the id of the one-to-one relation is of type OneToOneField
#             # try:
#             model_as_dict[field_name] = model_to_dict(field_value)
#             # except:
#             #     logger.error("Error converting one-to-one field.  field name is '%s', field type is '%s', value type is '%s', value is '%s', getattr is '%s'" % (
#             #         field_name,
#             #         ONE_TO_ONE_TYPE,
#             #         class_fullname(type(field_value)),
#             #         field_value,
#             #         getattr(model_obj, field_name)
#             #     ))
#             #     raise
#         elif isinstance(field_value, decimal.Decimal):
#             model_as_dict[field_name] = float(field_value)
#         elif type(field_value) == datetime.datetime:
#             # model_as_dict[field_name] = field_value.strftime(date_format)
#             model_as_dict[field_name] = field_value.isoformat()
#     return model_as_dict


# Save a model object from a json string
def deep_deserialize(json_str, model_obj_type):
    import json
    if json_str is None or not isinstance(json_str, basestring) or len(json_str) == 0:
        return None
    return deep_deserialize_from_dict(json.loads(json_str), model_obj_type)


# Save a model object from a dictionary object
def deep_deserialize_from_dict(dikt, model_obj_type):
    import copy
    import decimal
    from django.db import IntegrityError
    # from mirus import utils as mirus_utils
    # from sf_aoc.utils import utils

    def is_dj_version(ver_in):
        if len(ver_in) == 0:
            raise Exception('need at least one to match with')
        import django
        major_matches = django.VERSION[0] == ver_in[0]
        minor_matches = len(ver_in) < 2 or django.VERSION[1] == ver_in[1]
        patch_matches = len(ver_in) < 3 or django.VERSION[2] == ver_in[2]
        return major_matches and minor_matches and patch_matches

    def recursive_delete(obj_to_delete, parent_fk_field_name):
        for field_name in obj_to_delete._meta.get_all_field_names():
            field = obj_to_delete._meta.get_field_by_name(field_name)[0]
            if class_fullname(type(field)) == "django.db.models.related.RelatedObject":
                for child in obj_to_delete.__getattribute__(field_name).all():
                    recursive_delete(child, field.field.name)
        obj_to_delete.delete()

    if not dikt:
        return None
    # logger.debug("model obj type = %s" % model_obj_type)
    # import pprint; logger.debug("before: %s" % pprint.pformat(dikt))
    FOREIGN_KEY_FIELD_TYPE = "django.db.models.fields.related.ForeignKey"
    CHILD_FIELD_TYPE = "django.db.models.related.RelatedObject"
    from packaging import version
    import django
    dj_ver = version.parse(django.get_version())
    if dj_ver < version.parse('1.9'):
        MANY_TO_ONE_REL_TYPE = 'django.db.models.fields.related.ManyToOneRel'
    elif dj_ver >= version.parse('1.9'):
        MANY_TO_ONE_REL_TYPE = 'django.db.models.fields.reverse_related.ManyToOneRel'
    else:
        raise Exception('should never be here')
    # ONE_TO_ONE_REL_TYPE = 'django.db.models.fields.related.OneToOneRel'
    ONE_TO_ONE_FIELD_TYPE = 'django.db.models.fields.related.OneToOneField'
    CHILD_FIELD_TYPES = [
        CHILD_FIELD_TYPE,
        MANY_TO_ONE_REL_TYPE,
        # ONE_TO_ONE_REL_TYPE,
        # ONE_TO_ONE_FIELD_TYPE,
    ]
    DATE_TIME_FIELD_TYPE = "django.db.models.fields.DateTimeField"
    DECIMAL_FIELD = "django.db.models.fields.DecimalField"
    dikt_copy = copy.copy(dikt)
    for input_field_name in dikt_copy.keys():
        # delete all fields in input dict that don't exist in the model
        if input_field_name not in model_obj_type._meta.get_all_field_names():
            del dikt_copy[input_field_name]
    child_fields = []
    for field_name in model_obj_type._meta.get_all_field_names():
        field = model_obj_type._meta.get_field_by_name(field_name)[0]
        field_type_str = class_fullname(type(field))
        # logger.debug('field_type_str = %s' % field_type_str)
        if field_name in dikt_copy.keys():
            if field_type_str == FOREIGN_KEY_FIELD_TYPE:
                if field_name.endswith("_id") and field_name[:-len("_id")] in dikt_copy.keys():
                    # as of django 1.7 the fk id field is included
                    del dikt_copy[field_name]
                else:
                    # dikt_copy[field_name] = field.related.parent_model.objects.get(pk=dikt_copy[field_name])
                    dikt_copy[field_name] = field.related.model.objects.get(pk=dikt_copy[field_name])
            # elif field_type_str == CHILD_FIELD_TYPE:
            elif field_type_str == ONE_TO_ONE_FIELD_TYPE:
                oto_child_obj = deep_deserialize_from_dict(copy.deepcopy(dikt[field_name]), field.related_model)
                dikt_copy[field_name] = oto_child_obj
            elif field_type_str in CHILD_FIELD_TYPES:
                child_fields.append(field)
                del dikt_copy[field_name]
            elif field_type_str == DATE_TIME_FIELD_TYPE and field.auto_now_add and dikt_copy[field_name] is None:
                del dikt_copy[field_name]
            elif field_type_str == DECIMAL_FIELD and dikt_copy[field_name]:
                # cast floats to str for decimal field
                dikt_copy[field_name] = decimal.Decimal(str(dikt_copy[field_name]))
        # else:
        #     if field_type_str not in [FOREIGN_KEY_FIELD_TYPE,
        #                               # CHILD_FIELD_TYPE,
        #                               DATE_TIME_FIELD_TYPE,
        #                               # ONE_TO_ONE_REL_TYPE,
        #     ] + CHILD_FIELD_TYPES:
        #         # if we don't explicitly set the field to None, then the constructor unfortunately
        #         #  sets it to empty string
        #         dikt_copy[field_name] = None
    # import pprint; logger.debug("after: %s" % pprint.pformat(dikt_copy))
    if "id" in dikt_copy.keys() and dikt_copy["id"] is not None:
        matching_instances = model_obj_type.objects.filter(id=dikt_copy["id"])
        if matching_instances.count() != 1:
            raise Exception("There should be one instance of type: %s id: %s, there are %s" % (model_obj_type, dikt_copy["id"], matching_instances.count()))
        matching_instances.update(**dikt_copy)
        instance = matching_instances.all()[0]
    else:
        # import pdb; pdb.set_trace()
        instance = model_obj_type(**dikt_copy)
    try:
        instance.clean()
        instance.save()
    except IntegrityError, ie:
        raise
        # raise Exception(utils.get_exception_wrap_message(ie, "Error saving %s with values %s." % (model_obj_type, dikt_copy)))
    # logger.debug("child fields = %s"%child_fields
    for child_field in child_fields:
        child_field_name = child_field.get_accessor_name()
        old_children = instance.__getattribute__(child_field_name).all()
        old_children_ids = set([child.id for child in old_children])
        new_children_ids = set([child_dikt.get("id", None) for child_dikt in dikt[child_field_name]])
        ids_diff = old_children_ids - new_children_ids
        for old_child in old_children:
            if old_child.id in ids_diff:
                recursive_delete(old_child, child_field.field.name)
        for new_child_dict in dikt[child_field_name]:
            # logger.debug("recursing into %s"%child_field.get_accessor_name()
            if child_field.field.name not in new_child_dict.keys() or new_child_dict[child_field.field.name] is None:
                new_child_dict[child_field.field.name] = instance.id
            deep_deserialize_from_dict(copy.deepcopy(new_child_dict), child_field.related_model)
    return instance


def exclude_from_dict(dikt, keys_to_exclude):
    import copy
    result = copy.deepcopy(dikt)
    for key_to_exclude in keys_to_exclude:
        if key_to_exclude in result:
            del result[key_to_exclude]
    return result


def class_fullname(clazz):
    return clazz.__module__ + "." + clazz.__name__
