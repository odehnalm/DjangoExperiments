import uuid

from django.db import models


class Job(models.Model):
    _job_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    def get_id(self):
        return str(self._job_id)
