from django.db import models
from parts.models import Store, Brand, DeviceType
from django.utils.translation import ugettext_lazy as _

class Employee(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'employee'
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
        ordering = ['name']

class Expendable(models.Model):
    type = models.ForeignKey(DeviceType, verbose_name=_('type'))
    brand = models.ForeignKey(Brand, verbose_name=_('brand'))
    model = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('model'))
    number = models.CharField(max_length=10, verbose_name=_('number'))

    def __unicode__(self):
        if self.model:
            return "(%s) %s %s" % (self.number, self.type.name, self.model)
        return "(%s) %s" % (self.number, self.type.name)

    class Meta:
        db_table = 'expendable'
        verbose_name = _('expendable')
        verbose_name_plural = _('expendables')
        ordering = ['type__name']

class ExpendableInStore(models.Model):
    store = models.ForeignKey(Store)
    expendable = models.ForeignKey(Expendable)
    count = models.IntegerField()

    def __unicode__(self):
        return "%s %s [%s]" % (self.expendable.type.name, self.expendable.model, self.store.name)

    class Meta:
        db_table = 'expendable_in_store'
        verbose_name = _('expendable in store')
        verbose_name_plural = _('expendables in store')
        ordering = ['id']
        unique_together = ('expendable', 'store')

class ExpandableInUse(models.Model):
    employee = models.ForeignKey(Employee)
    expendable = models.ForeignKey(Expendable)
    date = models.DateField(auto_now_add=True, auto_now=True)
    task = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s %s [%s]" % (self.expendable.type.name, self.expendable.model, self.employee.name)