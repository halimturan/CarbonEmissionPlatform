from django.shortcuts import render
from apps.company.models import CompanyUser


def overview(request):
    company = CompanyUser.objects.filter(user=request.user).first()
    context = {
        'company': company,
    }
    return render(request, 'portal/company/overview.html', context)