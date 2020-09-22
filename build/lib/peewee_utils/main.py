from peewee import ForeignKeyField


_clone_set = lambda s: set(s) if s else set()

def prefetch_to_dict(model, recurse=True, backrefs=True, max_depth=None, exclude=None, __seen=None, __parent=None):
    """
    Convert a model instance (and any related objects) to a dictionary, without querying.

    :param bool recurse: Whether foreign-keys should be recursed.
    :param bool backrefs: Whether lists of related objects should be recursed.
    :param exclude: A list (or set) of field instances that should be
        excluded from the dictionary.
    :param int max_depth: Maximum depth to recurse, value <= 0 means no max.
    """
    data = {}
    max_depth = -1 if max_depth is None else max_depth
    if max_depth == 0:
        recurse = False
        backrefs = False
    if __parent is None:
        __parent = model
    elif __parent == model:
        return __parent._pk

    exclude = _clone_set(exclude)
    __seen = _clone_set(__seen)
    exclude |= __seen
    model_class = type(model)

    for field in model._meta.sorted_fields:
        field_data = model.__data__.get(field.name)
        if isinstance(field, ForeignKeyField):
            if field_data is not None and recurse:
                if (
                    field.name in model.__rel__
                ):
                    __seen.add(field)
                    rel_obj = getattr(model, field.name)
                    field_data = prefetch_to_dict(
                        rel_obj,
                        recurse=recurse,
                        backrefs=backrefs,
                        exclude=exclude,
                        max_depth=max_depth - 1,
                        __seen=__seen,
                        __parent=__parent,
                        )
            else:
                field_data = None

        data[field.name] = field_data

    # backref
    if backrefs:
        for foreign_key in model._meta.backrefs.keys():
            related_query = getattr(model, foreign_key.backref)
            if not isinstance(related_query, list):
                continue
            descriptor = getattr(model_class, foreign_key.backref)
            if descriptor in exclude or foreign_key in exclude:
                continue

            accum = []
            exclude.add(foreign_key)

            for item in related_query:
                accum.append(
                    prefetch_to_dict(
                        item,
                        recurse=recurse,
                        backrefs=backrefs,
                        exclude=exclude,
                        max_depth=max_depth - 1,
                        __parent=__parent,
                    )
                )

            data[foreign_key.backref] = accum

    return data
