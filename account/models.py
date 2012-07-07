from django.db import models
from django.contrib.admin.models import User as AuthUser
from parts.models import Store
from django.utils.translation import ugettext_lazy as _

class User(models.Model):
    user = models.ForeignKey(AuthUser)
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return "%s [%s]" % (self.user.username, self.store.name)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'
