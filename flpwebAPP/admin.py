from django.contrib import admin

# Register your models here.
from flpwebAPP.models import Matriz, Simulacion, Solucion

admin.site.register(Matriz)
admin.site.register(Simulacion)
admin.site.register(Solucion)