from django.shortcuts import render
from django import views


class Overview(views.generic.ListView):
    admin = {}

    def get(self, request):
        ctx = self.admin.each_context(request)
        ctx["full_name"] = "Full Name"
        ctx["email"] = "Email"
        return render(request, "overview.html", ctx)
