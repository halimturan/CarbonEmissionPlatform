from django.shortcuts import render
from apps.pricing.models import Plan
from apps.company.models import CompanyUser
from django.contrib.auth.decorators import login_required


def plans(request):
    plans = Plan.objects.all()
    return render(request, 'web/pricing/plans.html', {"plans": plans})


@login_required
def payment(request, slug):
    company = CompanyUser.objects.filter(user=request.user).first()
    plan = Plan.objects.get(slug=slug)
    return render(request, 'web/pricing/payment.html', {"plan": plan, "company": company})
