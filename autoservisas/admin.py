from django.contrib import admin
from .models import Gamintojas, Modelis, Klientas, Masina, Paslauga, Uzsakymas, UzsakymoEilute

admin.site.register(Gamintojas)
admin.site.register(Modelis)
admin.site.register(Klientas)
admin.site.register(Masina)
admin.site.register(Uzsakymas)
admin.site.register(Paslauga)
admin.site.register(UzsakymoEilute)
