from django.contrib import admin
from django.urls import path

from finders import views


class CustomAdminSite(admin.AdminSite):

    def get_urls(self):
        self._registry = admin.site._registry
        admin_urls = super().get_urls()
        custom_urls = [
            path(
                "overview/",
                views.Overview.as_view(admin=self),
                name="overview",
            ),
            # path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
        ]
        return custom_urls + admin_urls  # custom urls must be at the beginning

    def get(self, request):
        request.current_app == self.name
        return super().get(request)

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # app_list += [
        #     {
        #         "name": "Overview",
        #         "app_label": "Overview",
        #         # "app_url": "/admin/test_view",
        #         "models": [
        #             {
        #                 "name": "Overview",
        #                 "object_name": "overview",
        #                 "admin_url": "/overview",
        #                 "view_only": True,
        #             }
        #         ],
        #     }
        # ]
        return app_list


admin_site = CustomAdminSite()
