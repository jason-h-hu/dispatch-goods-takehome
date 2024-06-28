from django.db import models
from django.urls import reverse
import uuid
from string import Template

class UserModel(models.Model):
    # NOTE: https://shinesolutions.com/2018/01/08/falsehoods-programmers-believe-about-names-with-examples/
    first_name = models.CharField(max_length=64, help_text='aka personal name')
    last_name = models.CharField(max_length=64, help_text='aka family name, surname')
    age = models.IntegerField()
    address = models.CharField(max_length=256)

    # Additional Fields: These aren't in the original spec, but 
    # allow for useful bookkeeping and organization
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return Template('$last_name, $first_name. $id').substitute(
            last_name=self.last_name, 
            first_name=self.first_name, 
            id=self.id
        )