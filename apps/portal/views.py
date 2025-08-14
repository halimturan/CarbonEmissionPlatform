from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.utils import complete_signup
from allauth.account.adapter import get_adapter
import logging, re
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from allauth.account import app_settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.portal.models import Profile

logger = logging.getLogger(__name__)
User = get_user_model()

def sign_up(request):
    if request.method != 'POST':
        return render(request, 'portal/signup.html')

    # 1) POST verilerini al, boşlukları temizle
    email      = (request.POST.get('email') or '').strip()
    password   = (request.POST.get('password') or '').strip()
    first_name = (request.POST.get('first_name') or '').strip()
    last_name  = (request.POST.get('last_name') or '').strip()
    company    = (request.POST.get('company_name') or '').strip()
    country    = (request.POST.get('country') or '').strip() or None
    city       = (request.POST.get('city') or '').strip() or None
    phone_raw  = (request.POST.get('phone') or '').strip()

    # 2) Basit doğrulamalar (forms kullanmadan)
    if not email or '@' not in email:
        messages.error(request, "Geçerli bir e-posta adresi giriniz.")
        return render(request, 'portal/signup.html', {'post': request.POST})

    # E-posta zaten var mı?
    if User.objects.filter(email__iexact=email).exists():
        messages.error(request, "Bu e-posta ile zaten bir kullanıcı var. Giriş yapmayı deneyin.")
        return render(request, 'portal/signup.html', {'post': request.POST})

    if not password:
        messages.error(request, "Şifre boş olamaz.")
        return render(request, 'portal/signup.html', {'post': request.POST})

    # Django'nun şifre politikası (zayıf şifreleri yakalar)
    try:
        validate_password(password)
    except ValidationError as e:
        messages.error(request, "Şifre uygun değil: " + "; ".join(e.messages))
        return render(request, 'portal/signup.html', {'post': request.POST})

    # Telefonu sayılara indir (opsiyonel alan ise None bırak)
    phone_digits = re.sub(r'\D+', '', phone_raw)
    try:
        phone_number = int(phone_digits) if phone_digits else None
    except ValueError:
        messages.error(request, "Telefon numarası formatı hatalı.")
        return render(request, 'portal/signup.html', {'post': request.POST})

    # 3) Username üret ve benzersizleştir
    base_username = email.split('@')[0] or 'user'
    username = base_username
    i = 1
    while User.objects.filter(username__iexact=username).exists():
        username = f"{base_username}{i}"
        i += 1

    # 4) Oluşturma + allauth akışı tek transaction içinde
    try:
        with transaction.atomic():
            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()

            Profile.objects.create(
                user=user,
                city_id=city,
                country_id=country,
                company_name=company,
                phone=phone_number,
            )

            # E-posta doğrulama sürecini başlat
            complete_signup(
                request,
                user,
                app_settings.EMAIL_VERIFICATION,
                get_adapter().get_signup_redirect_url(request),
            )

    except IntegrityError:
        messages.error(request, "Aynı bilgilerle kayıt var gibi görünüyor. Lütfen farklı bir e-posta ile deneyin.")
        logger.exception("IntegrityError during sign_up")
        return render(request, 'portal/signup.html', {'post': request.POST})
    except Exception as e:
        messages.error(request, "Kayıt sırasında beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.")
        logger.exception("Unexpected error during sign_up: %s", e)
        return render(request, 'portal/signup.html', {'post': request.POST})

    messages.success(request, "Kayıt başarılı! Lütfen e-postanızı doğrulayın.")
    return redirect('/accounts/confirm-email/')


@login_required
def logout(request):
    return redirect("portal:login")


@login_required
def index(request):
    return render(request, 'portal/index.html')