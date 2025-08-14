from django.shortcuts import render
from apps.company.models import CompanyUser


def overview(request):
    company = CompanyUser.objects.all()
    return render(request, 'portal/company/overview.html')