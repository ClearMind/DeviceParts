from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class PartType(models.Model):
    name = models.CharField(max_length=24, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('part type')
        verbose_name_plural = _('part types')
        db_table = "part_type"
        ordering = ['name']


class DeviceType(models.Model):
    name = models.CharField(max_length=24, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("device type")
        verbose_name_plural = _("device types")
        db_table = "device_type"
        ordering = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")
        db_table = "brand"
        ordering = ['name']


class Device(models.Model):
    number = models.CharField(max_length=12, verbose_name=_('inventory number'))
    type = models.ForeignKey(DeviceType, verbose_name=_('type'))

    def __unicode__(self):
        return "(%s) %s" % (self.number, self.type.name)

    class Meta:
        verbose_name = _("device")
        verbose_name_plural = _('devices')
        db_table = 'device'
        ordering = ['id']


class Part(models.Model):
    type = models.ForeignKey(PartType, verbose_name=_('type'))
    brand = models.ForeignKey(Brand, verbose_name=_('brand'))
    model = models.CharField(max_length=32, verbose_name=_('model'), blank=True, null=True)
    number = models.CharField(max_length=10, verbose_name=_('number'))
    create_date = models.DateField(auto_now_add=True, verbose_name=_('date of creation'))

    def __unicode__(self):
        if self.model:
            return "(%s) %s %s" % (self.number, self.type.name, self.model)
        return "(%s) %s" % (self.number, self.type.name)

    class Meta:
        db_table = 'part'
        verbose_name = _('part')
        verbose_name_plural = _('parts')
        ordering = ['type__name']


class Store(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')
        db_table = "store"
        ordering = ['name']

class PartInStore(models.Model):
    part = models.ForeignKey(Part, verbose_name=_('part'))
    store = models.ForeignKey(Store, verbose_name=_('store'))
    count = models.IntegerField(verbose_name=_('count'))

    def __unicode__(self):
        return "%s [%s]" % (self.part.__unicode__(), self.store.name)

    class Meta:
        db_table = "part_in_store"
        verbose_name = _('part in store')
        verbose_name_plural = _('parts in store')
        unique_together = ('part', 'store')
        ordering = ['part', 'store', 'count']


class PartInDevice(models.Model):
    part = models.ForeignKey(Part)
    device = models.ForeignKey(Device)
    date = models.DateField(auto_now=True)
    user = models.ForeignKey(User)
    task = models.IntegerField(blank=True, null=True)
    act = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return "%s in %s" % (self.part.__unicode__(), self.device.__unicode__())

    class Meta:
        verbose_name = _('part in device')
        verbose_name_plural = _('parts in devices')
        db_table = "part_in_device"

class PartsInDevice:
    def __init__(self, device):
        self.parts = PartInDevice.objects.filter(device=device)

    def count(self):
        return self.parts.count()

    def __unicode__(self):
        return self.parts
