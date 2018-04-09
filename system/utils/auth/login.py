from allauth.account.adapter import get_adapter
from allauth.account.utils import perform_login

from apps.users.models import User


def perform_login(request, user):

    adapter = get_adapter(request)
    adapter.login(request, user)


def perform_ma_login(request, username_or_email, _kwargs):

	company = _kwargs.get('company', '')

	wrapper_user = User.objects.filter(
		username=username_or_email.lower(),
		macompany__name=company.upper(),
	)

	if wrapper_user.exists():
		user = wrapper_user[0]
		perform_login(request, user)
		return user

	return None