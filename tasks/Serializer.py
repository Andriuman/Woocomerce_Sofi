from rest_framework import serializers
from .models import UsuarioCuenta, Transaccion

class UsuarioCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioCuenta
        fields = '__all__'



class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'
