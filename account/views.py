from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from parts.views import base_context
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def login(request):
    c = base_context(request)
    c['title'] = _('Login')
    c['form'] = AuthenticationForm()

    c['next'] = request.GET.get('next', '/')

    template = get_template("registration/login.html")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(request.POST.get('next', "/"))
        else:
            c['form'] = form

    return HttpResponse(template.render(Context(c)))

def logout(request):
    auth_logout(request)

    return HttpResponseRedirect('/accounts/login/')