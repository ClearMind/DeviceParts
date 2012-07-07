from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from parts.views import base_context

def root(request):
    c = base_context(request)

    template = get_template("base.html")

    return HttpResponse(template.render(Context(c)))