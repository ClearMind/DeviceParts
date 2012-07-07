from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from expendables.models import ExpendableInStore
from parts.views import base_context
from django.utils.translation import ugettext_lazy as _

@login_required
def all(request):
    c = base_context(request)

    c['expendables'] = ExpendableInStore.objects.all()
    c['title'] = _('All expendables')
    c['jscripts'] = ['index.js']

    template = get_template("all_exp.html")

    return HttpResponse(template.render(Context(c)))

