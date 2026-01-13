from django.db import models
from django.contrib.auth.models import User

# --- Tablas de Ubicación y Organización ---
class Provincia(models.Model):
    nombre = models.CharField(max_length=45) # [cite: 553]
    descripcion = models.CharField(max_length=45) # [cite: 554]

class Departamento(models.Model):
    nombre = models.CharField(max_length=45) # [cite: 531]
    descripcion = models.CharField(max_length=45) # [cite: 531]
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE) # [cite: 469, 470]

class Localidad(models.Model):
    nombre = models.CharField(max_length=45) # [cite: 529]
    cp = models.CharField(max_length=45) # [cite: 529]
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE) # [cite: 466, 469]

class Jardin(models.Model):
    razon_social = models.CharField(max_length=45) # [cite: 547]
    direccion = models.CharField(max_length=45) # [cite: 547]
    telefono = models.CharField(max_length=45) # [cite: 547]
    cuil = models.CharField(max_length=45) # [cite: 548]
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE) # [cite: 543]

# --- Gestión de Usuarios (Tutor y Niño) ---
class PerfilUsuario(models.Model):
    # Extensión del usuario de Django para RF-01 y RF-02
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 
    dni = models.CharField(max_length=8) # [cite: 524]
    direccion = models.CharField(max_length=100) # [cite: 535]
    telefono = models.CharField(max_length=15) # [cite: 536]
    tipo = models.CharField(max_length=45) # [cite: 537]
    jardin = models.ForeignKey(Jardin, on_delete=models.SET_NULL, null=True) # [cite: 461, 462]

class Nino(models.Model):
    # Basado en RF-07 y Registro de Niños
    nombre = models.CharField(max_length=45) # [cite: 48]
    apellido = models.CharField(max_length=45) # [cite: 48]
    dni = models.CharField(max_length=45) # [cite: 48]
    domicilio = models.CharField(max_length=100) # [cite: 48]
    fecha_nacimiento = models.DateField() # [cite: 169]
    tutor = models.ForeignKey(User, on_delete=models.CASCADE) # [cite: 173]

# --- Módulo de Narraciones y Pictogramas ---
class Cuento(models.Model):
    nombre = models.CharField(max_length=45) # [cite: 561]
    descripcion = models.CharField(max_length=45) # [cite: 562]
    imagen = models.CharField(max_length=45) # [cite: 562]
    cantidad_palabras = models.CharField(max_length=45) # [cite: 562]
    categoria_edad = models.CharField(max_length=45) # [cite: 562]

class Pictograma(models.Model):
    # Clave para el RF-04 y RF-06
    descripcion = models.CharField(max_length=45) # [cite: 564]
    tipo_imagen = models.CharField(max_length=45) # [cite: 566]
    tamano = models.CharField(max_length=45) # [cite: 566]
    cuento = models.ForeignKey(Cuento, on_delete=models.CASCADE) # [cite: 504, 510]

class Reporte(models.Model):
    # Para la Gestión de Reportes (Pág 17)
    fecha = models.DateField() # [cite: 574]
    hora = models.TimeField() # [cite: 575]
    nino = models.ForeignKey(Nino, on_delete=models.CASCADE) # [cite: 295, 301]