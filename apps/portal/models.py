from django.contrib.auth.models import User
from django.db import models
from apps.web.models import Country, City


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    phone = models.BigIntegerField(verbose_name="Telefon")
    company_name = models.CharField(max_length=300, verbose_name="Şirket İsmi")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='Ülke')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Şehir")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Profiller"