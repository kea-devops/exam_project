from django.db import models
# Create your models here.


class UniqueID(models):
    @classmethod
    def generate_unique_id(cls):
        return cls.objects.create()

    def __str__(self):
        return str(self.pk)
