from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image
from tinymce.models import HTMLField


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
    vin_kodas = models.CharField('VIN kodas', max_length=17, unique=True, default='Cia turi buti unikalus kodas')
    cover = models.ImageField('Nuotrauka', upload_to='photos', null=True, blank=True)
    aprasymas = HTMLField(null=True, blank=True)

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
    # pilna_kaina = models.DecimalField('Pilna kaina', max_digits=8, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    uzsakovas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    grazinimo_terminas = models.DateField('Grazinimo terminas', null=True, blank=True)

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

    @property
    def yra_pradelstas(self):
        if self.grazinimo_terminas and date.today() > self.grazinimo_terminas:
            return True
        else:
            return False

    @property
    def skaiciuoti_pilna_kaina(self):
        suma = 0
        for eilute in self.uzsakymoeilute_set.all():
            suma += eilute.skaiciuoti_paslaugu_kaina
        return suma

    def __str__(self):
        return f"{self.statusas} {self.masina} {self.date}, kaina: {self.skaiciuoti_pilna_kaina}"

    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE)
    kiekis = models.PositiveIntegerField('Kiekis')
    paslauga = models.ForeignKey(Paslauga, on_delete=models.CASCADE)
    # paslaugu_kaina = models.DecimalField('Paslaugu kaina', max_digits=7, decimal_places=2, null=True, blank=True)

    @property
    def skaiciuoti_paslaugu_kaina(self):
        res = self.paslauga.kaina * self.kiekis
        return res

    def __str__(self):
        return f"{self.paslauga}"

    class Meta:
        verbose_name = "Uzsakymo eilute"
        verbose_name_plural = "Uzsakymo eilutes"


class UzsakymasReview(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Komentaras', max_length=1000)
    uzsakymas = models.ForeignKey(Uzsakymas, on_delete=models.CASCADE, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.date_created}, {self.reviewer}, {self.uzsakymas}, {self.content}'


class Profile(models.Model):
    picture = models.ImageField(upload_to='profile_pics', default='default-profile.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} profilis'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture.path:
            img = Image.open(self.picture.path)
            thumb_size = (150, 150)
            img.thumbnail(thumb_size)
            img.save(self.picture.path)
