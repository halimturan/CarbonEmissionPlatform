from django.contrib.gis.db import models
from apps.common.mixins.audit import AuditMixin
from parler.models import TranslatableModel, TranslatedFields
import uuid


class Sector(TranslatableModel, AuditMixin):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name="İsim"),
        description=models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sektörler"


class ActivityArea(AuditMixin, TranslatableModel):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, verbose_name="Sektor", related_name="activity_sector")
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name="İsim"),
        description=models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Faaliyet Alanları"


class Company(AuditMixin, TranslatableModel):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="İsim"),
        description=models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )
    logo = models.ImageField(upload_to='portal/company/logo', null=True, blank=True, verbose_name="Logo")
    address = models.CharField(verbose_name="Adres", max_length=1000, null=True, blank=True)
    geo = models.GeometryField(null=True, blank=True, verbose_name="Geometri", srid=4326)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ŞirketLer"


class Facilities(AuditMixin, TranslatableModel):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, verbose_name="Şirket", on_delete=models.CASCADE, related_name="facilities_company")
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="İsim"),
        description=models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )
    activities = models.ManyToManyField(ActivityArea, verbose_name="Faaliyet Alanları", related_name="facilities_activities", blank=True)
    address = models.CharField(verbose_name="Adres", max_length=1000, null=True, blank=True)
    geo = models.GeometryField(null=True, blank=True, verbose_name="Geometri", srid=4326)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tesisler"


class CompanyUser(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Firma")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Kullanıcı")

    def __str__(self):
        return f"{self.company} {self.user.username}"

    class Meta:
        verbose_name_plural = "Şirket Kullanıcı İlişkileri"