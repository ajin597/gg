from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

class RazorpayPayment(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)

    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
   

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"