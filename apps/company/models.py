from django.contrib.gis.db import models
from apps.common.mixins.audit import AuditMixin
from parler.models import TranslatableModel, TranslatedFields
from apps.web.models import Country, City
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
    country = models.ForeignKey(Country, verbose_name="Ülke", on_delete=models.CASCADE, related_name="company_country", blank=True, null=True)
    city = models.ForeignKey(City, verbose_name="Şehir", on_delete=models.CASCADE, related_name="city_country", blank=True, null=True)
    tax_no = models.BigIntegerField(verbose_name="Vergi Numarası", null=True, blank=True)
    phone = models.BigIntegerField(verbose_name="Telefon", null=True, blank=True)
    website = models.URLField(verbose_name="Website", null=True, blank=True)
    mail = models.EmailField(verbose_name="Email", null=True, blank=True)
    personnel_count = models.SmallIntegerField(verbose_name="Personel Sayısı", default=0)
    building_count = models.SmallIntegerField(verbose_name="Bina Sayısı", default=0)
    logo = models.ImageField(upload_to='portal/company/logo', null=True, blank=True, verbose_name="Logo")
    address = models.CharField(verbose_name="Adres", max_length=1000, null=True, blank=True)
    geo = models.GeometryField(null=True, blank=True, verbose_name="Geometri", srid=4326)

    def __str__(self):
        return self.name

    def profile_completion(self):
        rate = 0
        company = Company.objects.get(pk=self.pk)
        rate += 5  if company.name else 0
        rate += 5 if company.country else 0
        rate += 5 if company.city else 0
        rate += 5 if company.tax_no else 0
        rate += 5 if company.personnel_count else 0
        rate += 5 if company.building_count else 0
        rate += 5 if company.logo else 0
        rate += 5 if company.address else 0
        rate += 5 if company.geo else 0
        rate += 20 if company.facilities_company else 0
        return rate

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