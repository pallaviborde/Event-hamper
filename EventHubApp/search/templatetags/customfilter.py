from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    my_dict = dictionary.__dict__
    return my_dict.get(key)
