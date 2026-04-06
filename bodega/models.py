from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Perfil(models.Model):
    MODO_TEMA = [
        ('dark', 'Oscuro'),
        ('light', 'Claro'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tema_preferido = models.CharField(max_length=10, choices=MODO_TEMA, default='dark')
    avatar = models.ImageField(upload_to='perfiles/', null=True, blank=True)

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=20, help_text="Ej: Kilogramos, Metros, Unidades")
    abreviatura = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    # Identificación
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código SKU")
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    
    # Dimensiones y Peso (Opcionales)
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Peso en kg")
    alto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="en cm")
    ancho = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="en cm")
    largo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="en cm")
    
    # Costos y Stock
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=5)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.sku}] {self.nombre}"

    @property
    def volumen(self):
        """Calcula el volumen ocupado si tiene dimensiones."""
        if self.alto and self.ancho and self.largo:
            return self.alto * self.ancho * self.largo
        return 0

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    capacidad_m3 = models.DecimalField(max_digits=10, decimal_places=2, help_text="Capacidad total en metros cúbicos")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='existencias')
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    posicion_pasillo = models.CharField(max_length=50, blank=True, help_text="Ej: Pasillo A, Estante 3")

    class Meta:
        unique_together = ('producto', 'bodega')
        verbose_name_plural = "Inventarios"

class Movimiento(models.Model):
    TIPO_MOVIMIENTO = [
        ('E', 'Entrada (Compra/Ajuste)'),
        ('S', 'Salida (Venta/Merma)'),
        ('T', 'Transferencia entre Bodegas'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='salidas')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='entradas')
    tipo = models.CharField(max_length=1, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    referencia_documento = models.CharField(max_length=100, blank=True, help_text="N° de Factura o Guía")
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.nombre} ({self.cantidad})"