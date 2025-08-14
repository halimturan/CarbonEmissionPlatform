from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from apps.common.mixins.audit import AuditMixin
from django.utils import timezone
from datetime import timedelta, datetime
from slugify import slugify


class Features(AuditMixin, TranslatableModel):
    """
    Planlarda sınır koymak istediğin yetenekler (örn: kullanıcı ekleme).
    """
    COUNT = "count"
    UNIT_CHOICES = [(COUNT, "Adet")]

    code = models.SlugField(max_length=50, unique=True)  # "user_add", "product_slots", "api_calls"
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="İsim"),
        description=models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )
    is_active = models.BooleanField(default=True, verbose_name="Durum")
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default=COUNT)

    # Kullanım periyodu (sıfırlanma)
    NEVER = "never"      # hiç sıfırlanmaz (ör: toplam kullanıcı sayısı limiti)
    MONTHLY = "monthly"  # her ay sıfırlanır (ör: aylık API çağrısı)
    DAILY = "daily"      # günlük sıfırlanır
    YEARLY = "yearly"
    RESET_CHOICES = [(NEVER, "Sıfırlanmaz"), (YEARLY, 'Yıllık'), (MONTHLY, "Aylık"), (DAILY, "Günlük")]
    reset_policy = models.CharField(max_length=20, choices=RESET_CHOICES, default=NEVER)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Özellikler"


class Plan(AuditMixin, TranslatableModel):
    billing_styles = (('aylik', 'Aylık'), ('yillik', 'Yıllık'))
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="İsim"),
        description=models.CharField(max_length=500, verbose_name="Açıklama", null=True, blank=True)
    )
    slug = models.CharField(max_length=300, unique=True, null=True, blank=True)
    alignment = models.SmallIntegerField(verbose_name="Sıra", default=1)
    is_active = models.BooleanField(default=True, verbose_name="Durum")
    price = models.SmallIntegerField(verbose_name="Ücret", default=0)
    billing_style = models.CharField(max_length=20, verbose_name="Ödeme Tipi", choices=billing_styles, default='aylik')
    #features = models.ManyToManyField(Features, verbose_name="Özellikler", related_name='plan_features')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["alignment"]
        verbose_name_plural = "Planlar"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, separator=' ')
        super(Plan, self).save(*args, **kwargs)


class PlanFeature(models.Model):
    """
    Plan X - Özellik Y eşleşmesi ve limit.
    limit=None → sınırsız demek.
    """
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan_features", verbose_name="Plan")
    feature = models.ForeignKey(Features, on_delete=models.CASCADE, related_name="in_plans", verbose_name="Özellik")
    limit = models.PositiveIntegerField(null=True, blank=True, verbose_name="Limit")  # None => Unlimited

    class Meta:
        unique_together = [("plan", "feature")]
        verbose_name_plural = "Plan Özellikleri"

    def __str__(self):
        lim = "Sınırsız" if self.limit is None else str(self.limit)
        return f"{self.plan} / {self.feature} = {lim}"


# Not: Burada "Organization/Account/Company" kavramı yoksa User'a da bağlayabilirsin.
class Organization(models.Model):
    name = models.CharField(max_length=150)
    #owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="owned_orgs")
    company = models.ForeignKey("company.Company", on_delete=models.CASCADE, related_name="organization_company", verbose_name="Şirket")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Organizasyonlar"


class Subscription(models.Model):
    """
    Bir organizasyonun aktif planı (tarihli).
    """
    ACTIVE = "active"
    CANCELED = "canceled"
    STATUS_CHOICES = [(ACTIVE, "Aktif"), (CANCELED, "İptal")]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Organizasyon")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name="Plan")
    started_at = models.DateTimeField(default=timezone.now, verbose_name="Başlangıç Tarihi")
    ends_at = models.DateTimeField(null=True, blank=True, verbose_name="Bitiş Tarihi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE, verbose_name="Durum")

    class Meta:
        verbose_name_plural = "Abonelikler"
        indexes = [models.Index(fields=["organization", "status"])]

    def __str__(self):
        return f"{self.organization} → {self.plan} ({self.status})"

    # ---- Limit/Periyot yardımcıları ----
    def plan_limit_for(self, feature_code: str):
        try:
            pf = PlanFeature.objects.select_related("feature","plan").get(
                plan=self.plan, feature__code=feature_code
            )
            return pf.limit  # None => sınırsız
        except PlanFeature.DoesNotExist:
            return 0  # planda yoksa 0 say (izin verme)

    def period_window_for(self, feature: Features, when=None):
        when = when or timezone.now()
        if feature.reset_policy == Features.NEVER:
            # Sistem başlangıcından sonsuza bir pencere
            start = timezone.make_aware(datetime(1970,1,1))
            end = timezone.make_aware(datetime(2999,12,31,23,59,59))
        elif feature.reset_policy == Features.MONTHLY:
            start = timezone.make_aware(datetime(when.year, when.month, 1))
            # sonraki ayın ilk günü - 1 saniye
            if when.month == 12:
                next_start = timezone.make_aware(datetime(when.year+1, 1, 1))
            else:
                next_start = timezone.make_aware(datetime(when.year, when.month+1, 1))
            end = next_start - timedelta(seconds=1)
        elif feature.reset_policy == Features.DAILY:
            start = timezone.make_aware(datetime(when.year, when.month, when.day))
            end = start + timedelta(days=1) - timedelta(seconds=1)
        else:
            start, end = when, when
        return start, end

    def used_amount(self, feature_code: str, when=None) -> int:
        try:
            feature = Features.objects.get(code=feature_code)
        except Features.DoesNotExist:
            return 0
        start, end = self.period_window_for(feature, when)
        agg = FeatureUsage.objects.filter(
            subscription=self, feature=feature,
            period_start=start, period_end=end
        ).aggregate(total=models.Sum("amount"))
        return agg["total"] or 0

    def remaining(self, feature_code: str, when=None):
        limit = self.plan_limit_for(feature_code)
        if limit is None:
            return None  # sınırsız
        return max(0, limit - self.used_amount(feature_code, when))

    def can_use(self, feature_code: str, amount: int = 1, when=None) -> bool:
        limit = self.plan_limit_for(feature_code)
        if limit is None:
            return True
        return self.used_amount(feature_code, when) + amount <= limit

    def add_usage(self, feature_code: str, amount: int = 1, when=None, strict=True):
        """
        Kullanım kaydı atar. strict=True ise limit aşımında Exception fırlatır.
        """
        when = when or timezone.now()
        feature = Features.objects.get(code=feature_code)
        start, end = self.period_window_for(feature, when)

        if strict and not self.can_use(feature_code, amount, when):
            raise ValueError(f"Limit aşıldı: {feature_code}")

        FeatureUsage.objects.create(
            subscription=self, feature=feature,
            period_start=start, period_end=end,
            amount=amount, at=when
        )


class FeatureUsage(models.Model):
    """
    Bir periyottaki (gün/ay/hiç) kullanım toplamını tutan kayıtlar.
    Aynı (subscription, feature, period_start, period_end) içinde
    birden fazla satır olabilir; SUM ile toplanır.
    """
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="usages", verbose_name="Abonelik")
    feature = models.ForeignKey(Features, on_delete=models.CASCADE, verbose_name="Özellik")
    period_start = models.DateTimeField(verbose_name="Periyot Başlangıcı")
    period_end = models.DateTimeField(verbose_name="Periyot Bitişi")
    amount = models.PositiveIntegerField(default=1, verbose_name="Miktar")
    at = models.DateTimeField(default=timezone.now, verbose_name="Tarih")

    def __str__(self):
        return f"{self.subscription}-{self.feature}-{self.amount}"

    class Meta:
        verbose_name_plural = "Özellik Kullanımları"
        indexes = [
            models.Index(fields=["subscription", "feature", "period_start", "period_end"]),
        ]