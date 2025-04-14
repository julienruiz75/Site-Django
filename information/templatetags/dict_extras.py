# information/templatetags/dict_extras.py

from django import template

register = template.Library()

@register.filter
def dict_get(dictionnaire, cle):
    """Accède à une valeur d’un dictionnaire avec une clé passée dynamiquement."""