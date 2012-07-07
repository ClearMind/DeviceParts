from django.contrib.admin import site
from account.models import User

site.register(User)
