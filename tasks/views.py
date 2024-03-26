
from django.http import HttpResponse
from .script_woocommerce import ejecutar_script


def vista_script(request):
    resultado_del_script = ejecutar_script()
    return HttpResponse(resultado_del_script)