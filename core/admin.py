from django.contrib import admin
from .models import Provincia, Departamento, Localidad, Jardin, PerfilUsuario, Nino, Cuento, Pictograma

# Registramos los modelos para gestionarlos desde la web
admin.site.register(Provincia)
admin.site.register(Jardin)
admin.site.register(Nino)
admin.site.register(Cuento)
admin.site.register(Pictograma)