from django.db import models


class Gamintojas(models.Model):
    pavadinimas = models.CharField('Gamintojo pavadinimas', max_length=20)

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = "Gamintojas"
        verbose_name_plural = "Gamintojai"


class Modelis(models.Model):
    pavadinimas = models.CharField('Modelio pavadinimas', max_length=20, help_text="Iveskite automobilio modelius")
    gamintojas = models.ForeignKey(Gamintojas, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = "Modelis"
        verbose_name_plural = "Modeliai"


class Klientas(models.Model):
    vardas = models.CharField('Vardas', max_length=20)
    pavarde = models.CharField('Pavarde', max_length=20)
    tel_numeris = models.CharField('Telefono numeris', max_length=9)

    def __str__(self):
        return f'{self.pavarde} {self.vardas} {self.tel_numeris}'

    class Meta:
        ordering = ('pavarde', 'vardas')
        verbose_name = "Klientas"
        verbose_name_plural = "Klientai"


class Masina(models.Model):
    reg_numeris = models.CharField('Registracijos numeris', max_length=6, unique=True)
    modelis = models.ForeignKey(Modelis, on_delete=models.CASCADE)
    klientas = models.ForeignKey(Klientas, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.reg_numeris}'

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Paslauga(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=50)
    kaina = models.DecimalField('Kaina', max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.pavadinimas}'

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class Uzsakymas(models.Model):
    masina = models.ForeignKey(Masina, on_delete=models.CASCADE)
    pilna_kaina = models.DecimalField('Pilna kaina', max_digits=8, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    UZSAKYMO_STATUS = (
        ('p', 'Priimtas'),
        ('v', 'Vykdomas'),
        ('a', 'Atliktas'),
    )

    statusas = models.CharField(
        'Statusas',
        max_length=1,
        choices=UZSAKYMO_STATUS,
        default='p',
        blank=True,
        help_text='Uzsakymo statusas'
    )

    def __str__(self):
        return f"{self.statusas} {self.masina} {self.masina.klientas} {self.date}"

    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE)
    kiekis = models.PositiveIntegerField('Kiekis')
    paslauga = models.ForeignKey(Paslauga, on_delete=models.CASCADE)
    paslaugu_kaina = models.DecimalField('Paslaugu kaina', max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.paslauga}"

    class Meta:
        verbose_name = "Uzsakymo eilute"
        verbose_name_plural = "Uzsakymo eilutes"
