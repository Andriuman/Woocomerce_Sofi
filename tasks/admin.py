from django.contrib import admin
from .models import UsuarioCuenta

from .models import Transaccion

# Register your models here.




class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('cuenta_origen','id', 'fecha_transaccion_formateada')
    
    def fecha_transaccion_formateada(self, obj):
        return obj.fecha_transaccion.strftime("%d-%m-%Y %H:%M:%S %Z")
    fecha_transaccion_formateada.admin_order_field = 'fecha_transaccion'  
    fecha_transaccion_formateada.short_description = 'Fecha de Transacción'  
    
admin.site.register(Transaccion, TransaccionAdmin)
admin.site.register(UsuarioCuenta)
