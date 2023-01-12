from django import template

from storage.models import Speciality

register = template.Library()


@register.simple_tag()
def get_specs():
    return Speciality.objects.all()
