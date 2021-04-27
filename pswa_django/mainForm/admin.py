import csv
from io import StringIO
from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import User, PresentationLog, Advisor, TeamInformation
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

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

    def addStudent(self, firstname: str, lastname: str):
        log = PresentationLog()
        log.save()

        logId = PresentationLog.objects.get(TeamId=log.TeamId)
        # Create TeamInformation object for User's TeamId
        teaminfo = TeamInformation(TeamId=logId)
        # NumberOfTeamMembers=1,
        # AdvisorId='',
        # Topic='',
        # GithubRepoLink='')
        teaminfo.save()

        #teamId = TeamInformation.objects.get(TeamId=teaminfo.TeamId)
        # Create User objects from passed in data
        user = User(#TeamId=teamId,
                    FullName=firstname + " " + lastname,
                    is_admin=False)
        # Eid='',
        # Password='',
        # Email='',

        user.save()

    def import_csv_user(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            # Credit to https://stackoverflow.com/questions/62912039/uploading-csv-file-django-using-a-form
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')

            repeated_lines = 0
            header_line = True
            for line in lines:
                # Split fields in file by comma
                fields = line.split(',')
                # If header line don't include it
                if header_line:
                    header_line = False
                else:
                    try:
                        # Check if object already exists
                        if User.objects.get(FullName=fields[1] + " " + fields[0]):
                            repeated_lines += 1
                        else:
                            self.addStudent(fields[1], fields[0])
                    # User has no objects so add everything
                    except ObjectDoesNotExist:
                        self.addStudent(fields[1], fields[0])
                        #self.message_user(request, "Your csv file has not been imported. Repeated names were detected")
                        #return redirect("..")
            if repeated_lines > 0:
                self.message_user(request, "Your csv file has been imported. " + str(repeated_lines) +
                                  " repeats were detected and not added.")
                return redirect("..")
            else:
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

            repeated_lines = 0
            header_line = True
            for line in lines:
                # Split fields in file by comma
                fields = line.split(',')
                # If header line don't include it
                if header_line:
                    header_line = False
                else:
                    try:
                        # Check if object already exists
                        if Advisor.objects.get(Name=fields[1] + " " + fields[0]):
                            repeated_lines += 1
                        else:
                            # Create Advisor objects from passed in data
                            advisor = Advisor(Name=fields[1] + " " + fields[0])
                            advisor.save()
                    # Advisor has no objects so add everything
                    except ObjectDoesNotExist:
                        # Create Advisor objects from passed in data
                        advisor = Advisor(Name=fields[1] + " " + fields[0])
                        advisor.save()
            if repeated_lines > 0:
                self.message_user(request, "Your csv file has been imported. " + str(repeated_lines) +
                                  " repeats were detected and not added.")
                return redirect("..")
            else:
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )