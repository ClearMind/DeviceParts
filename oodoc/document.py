# -*- coding: utf-8 -*-

import  os
import uno
from com.sun.star.uno import Exception as UnoException
from com.sun.star.task import ErrorCodeIOException
from settings import MEDIA_ROOT, MEDIA_URL
from parts.models import Device, PartsInDevice, PartInDevice

# soffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --norestore -nofirstwizard --nologo --headless &

def get_document(file_name):
    path = os.path.join(MEDIA_ROOT, "template_docs/" + file_name)

    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)

    document = None
    try:
        context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
        document = desktop.loadComponentFromURL("file://" + path, "_blank", 0, ())
    except UnoException, e:
        return None

    return document


def replace(document, what, for_what):
    """ replace $what to for_what
    """
    ReplaceDescr = document.createReplaceDescriptor()
    ReplaceDescr.SearchString = "$%s" % what
    ReplaceDescr.ReplaceString = for_what
    document.replaceAll(ReplaceDescr)


def generate(document, values, save_to):
    for k in values.keys():
        replace(document, k, values[k])

    file_name = 'file://' + save_to
    if file_name[-4:] != '.odt':
        file_name += '.odt'
    try:
        document.storeAsURL(file_name, ())
    except ErrorCodeIOException, e:
        print e

    return file_name


def fill_data(keys, obj):
    data = {}
    for k in keys:
        data[k] = getattr(obj, k, "<!!>")

    return data


def install_act(device):
    document = get_document('act.odt')
    if document:
        path = os.path.join(MEDIA_ROOT, "docs/") + device.number

        pid = PartsInDevice(device)
        if pid.count() < 1:
            document.dispose()
            return ""

        data = {}

        user = pid.parts[0].user
        data['who'] = "%s. %s" % (user.first_name[0], user.last_name)
        data['inventory_number'] = device.number
        data['device_type'] = device.type.name
        data['date'] = pid.parts[0].date.strftime('%d.%m.%Y')
        i = 1
        for p in pid.parts:
            data[str(i)] = "%s. %s           (%s)" % (str(i), p.part.type.name + " " + p.part.model , p.part.number)
            i += 1

        while i < 10:
            data[str(i)] = ""
            i += 1

        res = generate(document, data, path)
        print res
        url = os.path.join(MEDIA_URL, "docs/" + device.number + ".odt")
        if res:
            return url
        document.dispose()
    return ''


