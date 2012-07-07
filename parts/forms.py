from django import forms
from django.utils.translation import ugettext_lazy as _
import datetime
from parts.models import DeviceType, PartInStore, Store

class InstallForm(forms.Form):
    task = forms.IntegerField( label=_("task"), required=False)
    inventory_number = forms.CharField(max_length=12, required=True, label=_('inventory number'))
    device_type = forms.ModelChoiceField(queryset=DeviceType.objects.all(), initial=1, label=_('device type'))
    install_date = forms.DateField(initial=datetime.date.today(), label=_('install date'))
#    part = forms.ModelChoiceField(queryset=PartInStore.objects.filter(count__gt=0), label=_('part'))


    def __init__(self, *args, **kwargs):
        super(InstallForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            if f.required:
                f.widget.attrs['class'] = 'required'


class ChangeStore(forms.Form):
    part = forms.ModelChoiceField(queryset=PartInStore.objects.filter(count__gt=0), label=_('part'))
    count = forms.IntegerField(min_value=1, label=_('count'), initial=1)
    to_store = forms.ModelChoiceField(queryset=Store.objects.all(), label=_('to store'))

    def __init__(self, *args, **kwargs):
        super(ChangeStore, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            if f.required:
                f.widget.attrs['class'] = 'required'