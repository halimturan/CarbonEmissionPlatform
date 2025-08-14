from apps.company.models import CompanyUser


def check_company_of_user(request):
    user_id = request.user.id
    check = CompanyUser.objects.filter(id=user_id).exists()
    return check
