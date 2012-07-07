from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.context import Context
import simplejson
from app.models import MenuItem
from parts.forms import InstallForm, ChangeStore
from parts.models import Part, PartInStore, Device, PartInDevice, Store
from django.middleware.csrf import get_token
from django.template.loader import get_template
import settings
from django.utils.translation import ugettext_lazy as _
from oodoc.document import install_act
from account.models import User as AccUser

def base_context(request):
    csrf_token = get_token(request)
    STATIC_URL = settings.STATIC_URL
    menu_items = MenuItem.objects.all()
    only_content = False
    if request.method == "GET":
        get = request.GET.copy()
        if get.get('only_content', 0):
            only_content = True

    return locals()

@login_required
def home(request):
    c = base_context(request)
    c['jscripts'] = ['index.js']
    gets = request.GET.copy()

    parts = ''
    if gets.has_key('store'):
        store=get_object_or_404(Store, id=gets['store'])
        parts = PartInStore.objects.filter(store=store)
    else:
        parts = PartInStore.objects.all()
    c['parts'] = parts

    template = get_template("index.html")

    return HttpResponse(template.render(Context(c)))

@login_required
def install(request):
    c = base_context(request)
    c['jscripts'] = ['jquery-ui-1.8.20.custom.min.js', 'chosen.jquery.min.js', 'install.js']
    c['csss'] = ['ui-lightness/jquery-ui-1.8.20.custom.css', 'chosen.css']

    sts = Store.objects.all()
    parts = {}
    for s in sts:
        pis = PartInStore.objects.filter(store=s, count__gt = 0)
        if pis:
            parts[s.name] = pis

    c['parts'] = parts

    if request.method != "POST":
        form = InstallForm(initial=request.GET)
        c['form'] = form
        if request.GET.has_key('inventory_number'):
            c['number'] = request.GET['inventory_number']
    else:
        form = InstallForm(request.POST)
        part_list = request.POST.getlist('parts')
        if len(part_list) < 1:
            c['parts_not_selected'] = True
        if request.POST.has_key('inventory_number'):
            c['number'] = request.POST['inventory_number']
        if form.is_valid():
            postdata = form.cleaned_data.copy()
            dev = None
            dev_inv_number = postdata.get('inventory_number', 0)
            dev_type = postdata.get('device_type', 0)
            if dev_inv_number != 0 and dev_type != 0:
                exist = Device.objects.filter(number=dev_inv_number)
                if exist.count() <= 0:
                    dev = Device()
                    dev.number = dev_inv_number
                    dev.type = dev_type
                    dev.save()
                else:
                    dev = exist[0]
            if dev:
                for p in part_list:
                    pis = PartInStore.objects.get(pk=p)

                    pid = PartInDevice()
                    pid.device = dev
                    pid.user = request.user
                    pid.date = postdata['install_date']
                    pid.part = pis.part
                    pid.task = postdata['task']
                    pid.save()
                    pis_count = pis.count
                    if pis_count > 0:
                        pis.count = pis_count - 1
                        pis.save()
                    c['message'] = _('Installation is done!')

        c['form'] = form

    template = get_template("install.html")

    return HttpResponse(template.render(Context(c)))

@login_required
def cancel(request, part_id):
    pid = get_object_or_404(PartInDevice, id=part_id)
    u = get_object_or_404(AccUser, user = pid.user)

    pis = get_object_or_404(PartInStore, part=pid.part, store=u.store)
    pis.count += 1
    pis.save()

    pid.delete()

    return HttpResponse('OK')



@login_required
def change_store(request):
    c = base_context(request)
    if not request.user.is_staff:
        c['have_not_grants'] = True

    form = ChangeStore()
    if request.method == 'POST':
        form = ChangeStore(request.POST)
        if form.is_valid():
            postdata = form.cleaned_data.copy()
            pis = postdata['part']
            store = postdata['to_store']
            count = postdata['count']

            if not (store.pk == pis.store.pk):
                have_pis = PartInStore.objects.filter(store=store).filter(part=pis.part)
                if have_pis:
                    have_pis = have_pis[0]
                    have_pis.count += min(count, pis.count)
                    have_pis.save()
                else:
                    new_pis = PartInStore()
                    new_pis.count = min(count, pis.count)
                    new_pis.part = pis.part
                    new_pis.store = store
                    new_pis.save()
                c['message'] = _('Transition is done!')

                cnt_post = pis.count - count
                if cnt_post < 1:
                    cnt_post = 0
                pis.count = cnt_post
                pis.save()

    c['form'] = form
    c['title'] = _('Part transition')

    template = get_template('change_store.html')

    return HttpResponse(template.render(Context(c)))

@login_required
def installed(request):
    c = base_context(request)
    c['jscripts'] = ['printer.js']

    gets = request.GET.copy()
    if gets.has_key("device"):
        device = get_object_or_404(Device, id=gets['device'])
        parts = PartInDevice.objects.filter(device=device)
        c['device'] = device
    elif gets.has_key('part'):
        part = get_object_or_404(Part, id=gets['part'])
        parts = PartInDevice.objects.filter(part=part)
    elif gets.has_key('user'):
        user = get_object_or_404(User, id=gets['user'])
        parts = PartInDevice.objects.filter(user=user)
    elif gets.has_key('date'):
        date_ = gets['date'].split("-")
        parts = PartInDevice.objects.filter(date=date(int(date_[0]), int(date_[1]), int(date_[2])))
    elif gets.has_key('number'):
        device = get_object_or_404(Device, number=gets['number'])
        parts = PartInDevice.objects.filter(device=device)
        c['device'] = device
    else:
        parts = PartInDevice.objects.all()

    c['parts'] = parts

    template = get_template("installed.html")

    return HttpResponse(template.render(Context(c)))

@login_required
def installed_in_device(request, device_number):
    c = base_context(request)
    c['jscripts'] = ['cancel.js']

    device = Device.objects.filter(number=device_number)
    if not device:
        c['not_found'] = True
        c['number'] = device_number
    else:
        device = device[0]

    parts = PartInDevice.objects.filter(device=device)

    c['device'] = device
    c['parts'] = parts

    template = get_template("installed_in_device.html")

    return HttpResponse(template.render(Context(c)))

# AJAX
@login_required
def devices(request):
    if request.method == 'GET':
        number = request.GET.get('number', False)
        if number:
            devs = Device.objects.filter(number=number)
        else:
            devs = Device.objects.all()
    map = []
    if devs:
        for d in devs:
            map.append([d.number, d.type_id])

    return HttpResponse(simplejson.dumps(map), mimetype="text/json")

def prnt(request):
    if request.method == 'GET':
        dev_id = request.GET.get('device', 0)
        dev = get_object_or_404(Device, id=dev_id)
        if not dev:
            return HttpResponse("No such device")
        url = install_act(dev)

        if url:
            return HttpResponse(url)
        else:
            raise Http404
    return HttpResponse('not GET')
