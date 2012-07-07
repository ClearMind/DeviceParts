from django.db import models
from django.utils.translation import ugettext_lazy as _

class MenuItem(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    url = models.CharField(max_length=32, verbose_name=_('URL'))
    order = models.IntegerField(verbose_name=_('order'))
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=_('parent menu'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')
        db_table = 'menu_item'
        ordering = ["order"]