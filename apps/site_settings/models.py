from django.db import models


class SiteSettings(models.Model):
    """General settings are here."""
    logo = models.FileField(upload_to="img/site_settings", verbose_name="Logo")
    shortcut = models.FileField(upload_to="img/site_settings", verbose_name="İkon")
    name = models.CharField(max_length=255, verbose_name="İsim")
    phone = models.CharField(max_length=50, verbose_name="Telefon")
    email = models.CharField(max_length=100, verbose_name="Mail")
    address = models.CharField(max_length=500, verbose_name="Adres")
    google_maps_link = models.CharField(max_length=1000, verbose_name="Google Maps Link")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = "Site Ayarları"
