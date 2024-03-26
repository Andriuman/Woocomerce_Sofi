from django.db import models
from django.core.validators import RegexValidator
from django.db import transaction
from django.core.exceptions import ValidationError

class UsuarioCuenta(models.Model):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo_electronico = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=50)
    fecha_creacion_usuario = models.DateTimeField(auto_now_add=True)
    celular = models.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')], max_length=17, blank=True)
    documento_identidad = models.CharField(max_length=20, unique=True, primary_key=True)
    numero_cuenta_bancaria = models.CharField(max_length=20, unique=True)
    tipo_cuenta_bancaria = models.CharField(max_length=20)  # Nuevo campo
    banco = models.CharField(max_length=50)  # Nuevo campo
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='USD')
    fecha_creacion_cuenta = models.DateTimeField(auto_now_add=True)

    def actualizar_saldo(self, monto):
        nuevo_saldo = self.saldo + monto
        if nuevo_saldo < 0:
            raise ValidationError("Fondos insuficientes.")
        self.saldo = nuevo_saldo
        self.save()

    def __str__(self):
        return f"{self.documento_identidad} - {self.nombre_usuario}"

class Transaccion(models.Model):
    numero_de_orden = models.CharField(max_length=50, unique=True, null=True)
    tipo = models.CharField(max_length=1, choices=[('D', 'Deposito')])
    cuenta_origen = models.ForeignKey(UsuarioCuenta, on_delete=models.CASCADE, related_name='transacciones_origen', null=True, blank=True)
    cuenta_destino = models.ForeignKey(UsuarioCuenta, on_delete=models.CASCADE, related_name='transacciones_destino', null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    moneda = models.CharField(max_length=3, default='USD')

    def __str__(self):
        tipo_transaccion = dict([('D', 'Deposito')]).get(self.tipo, "Depósito")
        return f"{tipo_transaccion} - {self.monto} {self.moneda} - Fecha: {self.fecha_transaccion.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args, **kwargs):
        if self.tipo == 'D' and self.cuenta_origen:
            saldo_origen_suficiente = self.cuenta_origen.saldo >= self.monto
            if not saldo_origen_suficiente:
                raise ValidationError("La cuenta de origen no tiene fondos suficientes para realizar esta transacción.")
        with transaction.atomic():
            if self.tipo == 'D':
                if self.cuenta_origen:
                    self.cuenta_origen.actualizar_saldo(-self.monto)
                self.cuenta_destino.actualizar_saldo(self.monto)
        super().save(*args, **kwargs)