from django import template

register = template.Library()


@register.filter(name='group_fields')
def group_fields(fields, groups):
    grouped_fields_dict = {
    }
    results = []
    for count, field in enumerate(fields):
        worked_field = False
        for group in groups.split(','):
            if field.label in group:
                grouped_fields_dict.setdefault(group, []).append(field)
                worked_field = True
                break
        if worked_field is False:
            grouped_fields_dict.setdefault(count, field)
    for key in list(grouped_fields_dict.keys()):
        results.append(grouped_fields_dict[key])
    return results


@register.filter(name='is_list')
def is_list(args):
    return type(args) == list
