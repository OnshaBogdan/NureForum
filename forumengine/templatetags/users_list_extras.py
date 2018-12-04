from django import template

register = template.Library()


@register.filter(name='order')
def order(self):
    return enumerate(self, 1)


@register.filter
def hash(h, key):
    return h[key]

@register.filter
def atindex(List, i):
    return List[int(i) - 1]
