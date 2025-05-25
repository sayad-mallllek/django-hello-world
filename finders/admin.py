from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import user_passes_test

from finders import views


# Define superuser check decorator
def superuser_required(view_func):
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser, login_url="admin:login"
    )(view_func)
    return decorated_view


class CustomAdminSite(admin.AdminSite):

    def get_urls(self):
        self._registry = admin.site._registry
        admin_urls = super().get_urls()
        custom_urls = [
            path(
                "overview/",
                superuser_required(views.Overview.as_view(admin=self)),
                name="overview",
            ),
            path(
                "range-summary/",
                superuser_required(views.RangeSummary.as_view(admin=self)),
                name="range_summary",
            ),
             path(
                "export-range-summary/",
                superuser_required(views.export_range_summary),
                name="export_range_summary",
            ),
            path(
                "shipping-provider-analyze/",
                superuser_required(views.ShippingProviderAnalyze.as_view(admin=self)),
                name="shipping_provider_analyze",
            ),
            path(
                "export-shipping-provider-analyze/",
                superuser_required(views.export_shipping_provider_analyze),
                name="export_shipping_provider_analyze",
            ),
            path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
        ]
        return custom_urls + admin_urls  # custom urls must be at the beginning

    def get(self, request):
        request.current_app == self.name
        return super().get(request)

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        if request.user.is_superuser:
            app_list += [
                {
                    "name": "Overview",
                    "app_label": "Overview",
                    # "app_url": "/admin/test_view",
                    "models": [
                        {
                            "name": "Overview",
                            "object_name": "overview",
                            "admin_url": "/overview",
                            "view_only": True,
                        },
                        {
                            "name": "Range Summary",
                            "object_name": "range_summary",
                            "admin_url": "/range-summary",
                            "view_only": True,
                        },
                        {
                            "name": "Shipping Provider Analyze",
                            "object_name": "shipping_provider_analyze",
                            "admin_url": "/shipping-provider-analyze",
                            "view_only": True,
                        },
                    ],
                }
            ]
        return app_list


admin_site = CustomAdminSite()
