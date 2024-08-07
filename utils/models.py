from datetime import datetime
from django.db import models
from django.db.models import Manager, QuerySet
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


class AppManager(Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db).exclude(is_deleted=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    def delete(self):
        """Mark the record as deleted instead of deleting it"""

        self.deleted_at = datetime.now()
        self.save(from_delete=True)  # type: ignore


class BaseAdminModel(admin.ModelAdmin, DynamicArrayMixin):
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.exclude(deleted_at=None)


class BaseAdminInline(admin.StackedInline):
    readonly_fields = ("created_at", "updated_at")
    classes = ["collapse"]
    per_page = 5

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.exclude(deleted_at=None)
