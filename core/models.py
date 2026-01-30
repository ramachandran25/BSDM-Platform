import uuid
from django.db import models

class UIDModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
