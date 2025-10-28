from django.db.models.fields import CharField

from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Students(UUIDBaseModel, CreatedBaseModel):
    first_name = CharField(max_length=100, null=True)
    last_name = CharField(max_length=100, null=True)
    phone = CharField(max_length=15, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

