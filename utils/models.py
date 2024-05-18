from datetime import timezone
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

        self.deleted_at = timezone.now()
        self.save()


class BaseAdminModel(admin.ModelAdmin, DynamicArrayMixin):
    readonly_fields = ("created_at", "updated_at")

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.exclude(deleted_at=None)


class BaseAdminTabularInline(admin.StackedInline):
    readonly_fields = ("created_at", "updated_at")

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.exclude(deleted_at=None)
