from django.contrib import admin
from .models import Categoria, Evento, Participante

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Evento)
admin.site.register(Participante)