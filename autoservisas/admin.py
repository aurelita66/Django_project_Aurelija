from django.contrib import admin
from .models import (Gamintojas, Modelis, Klientas, Masina, Paslauga, Uzsakymas, UzsakymoEilute,
                     UzsakymasReview, Profile)


class UzsakymoEiluteInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('masina', 'uzsakovas', 'date', 'statusas', 'grazinimo_terminas')
    list_editable = ('uzsakovas', 'statusas', 'grazinimo_terminas')
    inlines = (UzsakymoEiluteInline,)


class MasinaAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'modelis__pavadinimas', 'reg_numeris')
    list_filter = ('klientas', 'modelis__pavadinimas')
    search_fields = ('reg_numeris', 'modelis__pavadinimas', 'klientas__pavarde')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


class ModelisAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'gamintojas')


admin.site.register(Gamintojas)
admin.site.register(Modelis, ModelisAdmin)
admin.site.register(Klientas)
admin.site.register(Masina, MasinaAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(UzsakymasReview)
admin.site.register(Profile)
