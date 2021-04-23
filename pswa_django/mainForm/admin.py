import csv
from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import User, PresentationLog, Advisor, TeamInformation

# Register your models here.
admin.site.register(TeamInformation)
admin.site.register(PresentationLog)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_list_template = "admin/users_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv-user/', self.import_csv_user),
        ]
        return my_urls + urls

    def import_csv_user(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    change_list_template = "admin/advisors_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv-advisor/', self.import_admin_csv),
        ]
        return my_urls + urls

    def import_admin_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )