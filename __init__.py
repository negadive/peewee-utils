from peewee import ForeignKeyField

__title__ = 'pyhumps'
__version__ = '1.3.1'
__author__ = 'Nick Ficano'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 Nick Ficano'


def prefetch_to_dict(model, parent=None):
    """
    Merubah hasil prefetch(list of object dengan backref juga list of object)
    menjadi dictionary tanpa query ke db
    """
    data = {}
    if parent is None:
        parent = type(model)
    else:
        return data

    for field in model._meta.sorted_fields:
        field_data = model.__data__.get(field.name)
        if isinstance(field, ForeignKeyField):
            if field_data is not None:
                if (
                    field.name in model.__rel__
                    and type(model.__rel__.get(field.name)) != parent
                ):
                    rel_obj = getattr(model, field.name)
                    field_data = prefetch_to_dict(rel_obj, parent=parent)
            else:
                field_data = None

        data[field.name] = field_data

    # backref
    accum = []
    for foreign_key in model._meta.backrefs.keys():
        related_query = getattr(model, foreign_key.backref)
        if not isinstance(related_query, list):
            continue

        for item in related_query:
            accum.append(
                prefetch_to_dict(item, parent=parent)
            )

        data[foreign_key.backref] = accum

    return data
