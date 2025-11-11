from django import template
from django.conf import settings
from qorder.models import *


register = template.Library()



@register.simple_tag
def si_no(value):
    if '1' in value:
        return "SI"
    elif '0' in value:
        return "NO"
    else:
        return "--"



@register.filter
def is_tipo_orden_enabled(value, username):
    try:
        user = EmserUser.objects.get(username=username)
        tou= QwConfigTiposOrdenesUsuarios.objects.filter(id_tipo_orden=value,
                                                   id_usuario=user)
        if tou.count()>0:
            return True
    except:
        return False



@register.assignment_tag
def get_config_tipo_orden(*args):
    try:
        return QwConfigTiposOrdenes.objects.filter(id_tipo_orden=args[0],
                                                   id_dato_config=args[1])[0]
    except:
        return False

@register.assignment_tag
def get_config_usuario(*args):
    from core.models import EmserUser
    try:
        user = EmserUser.objects.get(username=args[1])
        return QwConfigTiposOrdenesUsuarios.objects.filter(id_tipo_orden=args[0],
                                                   id_usuario=user)[0]
    except:
        return False
@register.simple_tag
def get_descrip_tipos_accion(cod):

    switcher = {
        "FOTO": "FOTO",
        "BARRAS": "CODIGO DE BARRAS",
        "MENSAJE": "MENSAJE",
        "ENCUESTA": "ENCUESTA",
        "VOZ": "MENSAJE DE VOZ",
        "TEXTO": "INGRESO DE TEXTO"
    }

    return switcher.get(cod, "Código incorrecto")

@register.filter
def restar(value, arg):
    try:
        return (int(value) if value is not None else 0) - (int(arg) if arg is not None else 0)
    except Exception:
        return value