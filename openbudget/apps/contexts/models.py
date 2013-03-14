from django.db import models
from django.utils.translation import ugettext_lazy as _
from openbudget.apps.entities.models import Entity
from openbudget.commons.mixins.models import PeriodicModel


class Context(PeriodicModel):

    entity = models.OneToOneField(
        Entity
    )

    # Geographical context

    # Population context

    # Social / economical context