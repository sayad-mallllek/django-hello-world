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
        try:
            # First try to get existing capital
            return cls.objects.get(pk=1)
        except cls.DoesNotExist:
            # If doesn't exist, create new one
            obj = cls(id=1, amount=0)
            obj.save()
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

    def save(self, *args, **kwargs):

        from_delete = kwargs.pop("from_delete", False)
        if from_delete:
            return super().save(*args, **kwargs)

        if self.pk:
            # Instance is being updated
            old_amount = Expense.objects.get(pk=self.pk).amount
        else:
            # Instance is being created
            old_amount = 0

        new_amount = self.amount
        amount_difference = old_amount - new_amount

        # You can now use amount_difference as needed
        # For example, logging the difference
        if amount_difference != 0:
            capital = Capital.objects.get(pk=1)
            capital.amount += amount_difference
            capital.save()

        super().save(*args, **kwargs)

    def delete(self):
        capital = Capital.objects.get(pk=1)
        capital.amount += self.amount
        capital.save()

        return super().delete()
