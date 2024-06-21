from django.db import models

from utils.models import BaseModel


class CapitalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(pk=1)

    def get_object(self):
        # return the single Capital instance
        return Capital.objects.get(pk=1)


# Create your models here.
class Capital(BaseModel):
    amount = models.FloatField()

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Capital, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, amount=0)
        print(created)
        return obj

    def __str__(self):
        return f"{self.amount}$"


class ExpenseCategory(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(BaseModel):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(null=True, blank=True)
    # category = models.CharField(null=True, blank=True, max_length=100)
    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
