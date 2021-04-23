import csv
from io import StringIO
from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import User, PresentationLog, Advisor, TeamInformation

# Register your models here.
admin.site.register(TeamInformation)
admin.site.register(PresentationLog)

# Credit to https://books.agiliq.com/projects/django-admin-cookbook/en/latest/import.html
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

# Credit to https://books.agiliq.com/projects/django-admin-cookbook/en/latest/import.html
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

            # Credit to https://stackoverflow.com/questions/62912039/uploading-csv-file-django-using-a-form
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            for line in lines:
                fields = line.split(',')
                if fields.count == 2:
                    # Create PresentationLog object for TeamInformation's LogId
                    log = PresentationLog()
                    log.save()
                    # Create TeamInformation object for User's TeamId
                    teaminfo = TeamInformation(TeamId=log.TeamId)
                                               #NumberOfTeamMembers=1,
                                               #AdvisorId='',
                                               #Topic='',
                                               #GithubRepoLink='')
                    teaminfo.save()
                    # Create User objects from passed in data
                    user = User(TeamId=teaminfo.TeamId, FirstName=fields[1], LastName=fields[0], is_admin=False)
                                #Eid='',
                                #Password='',
                                #Email='',

                    user.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

# Credit to https://books.agiliq.com/projects/django-admin-cookbook/en/latest/import.html
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

            # Credit to https://stackoverflow.com/questions/62912039/uploading-csv-file-django-using-a-form
            file_data = csv_file.read().decode('utf-8')
            # Split lines in file by new line character
            lines = file_data.split('\n')
            for line in lines:
                # Split fields in file by comma
                fields = line.split(',')
                # Create Advisor objects from passed in data
                advisor = Advisor(Name=fields[1] + " " + fields[0])
                advisor.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )