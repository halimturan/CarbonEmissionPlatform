from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from apps.common.mixins.audit import AuditMixin
from ckeditor.fields import RichTextField


class SubMenu(AuditMixin, TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=100, verbose_name="İsim"),
        description = models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )
    icon = models.FileField(upload_to="web/header/nav/menu_items", verbose_name="İkon", null=True, blank=True)
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)
    link = models.CharField(verbose_name="Link", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Alt Menüler"


class MenuItem(AuditMixin, TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=100, verbose_name="İsim"),
        link = models.CharField(max_length=500, verbose_name="Link", null=True, blank=True)
    )
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)
    sub_menu = models.ManyToManyField(SubMenu, verbose_name="Alt Menüler", blank=True, related_name="menu_items")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Menüler"


class Sliders(AuditMixin, TranslatableModel):
    image_allignment_list = (('left', 'Sol'), ('right', 'Sağ'))
    translations = TranslatedFields(
        text = RichTextField(verbose_name="Metin"),
        button_text = models.CharField(max_length=100, verbose_name="Buton Text", null=True, blank=True),
        link = models.CharField(verbose_name="Link", null=True, blank=True)
    )
    image = models.FileField(upload_to="web/sliders", verbose_name="Resim", null=True, blank=True)
    image_alignment = models.CharField(max_length=10, verbose_name="Resim Konumu", choices=image_allignment_list)
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)
    has_redirect = models.BooleanField(default=False, verbose_name="Yönlendirme var mı?")
    is_publish = models.BooleanField(default=False, verbose_name="Yayınlansın mı?")

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Sliderlar"


class FAQ(AuditMixin, TranslatableModel):
    """Frequently Asked Questions."""
    translations = TranslatedFields(
        question=models.CharField(max_length=300, verbose_name='Soru'),
        answer=models.CharField(max_length=2000,  verbose_name="Cevap")
    )
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Sıkça Sorulan Sorular"


class WhyUse(AuditMixin, TranslatableModel):
    icon = models.FileField(upload_to="web/why_use/icons")
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name='Başlık'),
        description=models.CharField(max_length=500,  verbose_name="Açıklama")
    )
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Neden Kullanmalıyız?"


class Features(AuditMixin, TranslatableModel):
    icon = models.FileField(upload_to="web/features/icons")
    translations = TranslatedFields(
        title=models.CharField(max_length=100, verbose_name='Başlık'),
        description=models.CharField(max_length=500, verbose_name='Açıklama'),
    )
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Özellikler"


class ContentBlock(AuditMixin, TranslatableModel):
    translations = TranslatedFields(
        text=RichTextField(verbose_name="Metin"),
        image=models.FileField(upload_to="web/content_block/images", verbose_name="Resim"),
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "İçerik Bloğu"


class Country(models.Model):
    name = models.CharField(max_length=100)
    country_id = models.SmallIntegerField(verbose_name="Ülke ID")
    iso2 = models.CharField(max_length=2)
    emoji = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ülkeler"


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Şehirler'
