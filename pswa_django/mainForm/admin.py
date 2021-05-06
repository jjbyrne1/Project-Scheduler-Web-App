from django import forms
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from mainForm.models.model_advisors import Advisor
from mainForm.models.model_team_informations import TeamInformation
from mainForm.models.model_students import Student
from mainForm.models.model_presentation_logs import PresentationLog


@admin.register(PresentationLog)
class PresentationLogAdmin(admin.ModelAdmin):
    # Sorts by a PresentationLog's TeamID field when displaying objects in PresentationLog admin page
    ordering = ('TeamID',)


def delete_teams_with_no_students(modeladmin, request, queryset):
    for team in queryset:
        if team.Students.count() == 0:
            modeladmin.message_user(request, f"{team} has {team.Students.count()} students")
            team.delete()


@admin.register(TeamInformation)
class TeamAdmin(admin.ModelAdmin):
    # Sorts by a TeamInformation's TeamID field when displaying objects in TeamInformation admin page
    ordering = ('TeamID',)

    actions = [delete_teams_with_no_students]

    # Used to remove any other occurrences of students on another teams, as students can only be assigned to one team
    def _response_post_save(self, request, obj):
        # Loop through all the team information objects
        for teaminfo in TeamInformation.objects.all().exclude(TeamID=obj.TeamID):
            # For each user in the changing objects User list
            for student in obj.Students.all():
                # For each User that was on the team before
                for original_student in teaminfo.Students.all():
                    if student.FullName == original_student.FullName:
                        t = TeamInformation.objects.get(TeamID=teaminfo.teamid)
                        t.Students.remove(student)
                        t.save()
                        if t.Students.count() == 0:
                            TeamInformation.objects.get(TeamID=teaminfo.teamid).delete()

        # Credit to https://docs.djangoproject.com/en/1.8/_modules/django/contrib/admin/options/
        opts = self.model._meta
        if self.has_change_permission(request, None):
            post_url = reverse('admin:%s_%s_changelist' %
                               (opts.app_label, opts.model_name),
                               current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)
        else:
            post_url = reverse('admin:index',
                               current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)


# Credit to https://books.agiliq.com/projects/django-admin-cookbook/en/latest/import.html
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


# Credit to https://books.agiliq.com/projects/django-admin-cookbook/en/latest/import.html
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Specifies the admin changelist template that we are extending to add an import csv link
    change_list_template = "admin/users_changelist.html"

    #list_display = ['FullName']

    # Sorts by a Students FullName field when displaying objects in Student admin page
    ordering = ('FullName',)

    # Adds a new url to mainForm's urls.py that can direct the user to a form to import a csv file
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv-user/', self.import_csv_user),
        ]
        return my_urls + urls

    # Function for creating a new student, generating a new team and adding the student to that team,
    # and generating a new presentation log with the previously generated team's teamid
    def add_student(self, lastname: str, firstname: str):
        # Create User objects from passed in data
        student = Student(FullName=f"{lastname}, {firstname}")
        student.save()

        # Create new TeamInformation object
        teaminfo = TeamInformation()
        teaminfo.save()

        teaminfo.Students.add(student)

        teamId = TeamInformation.objects.get(TeamID=teaminfo.teamid)

        # Create new default Presentation Log object
        log = PresentationLog(TeamID=teamId)
        log.save()

    # Executed for deleting multiple students
    def delete_queryset(self, request, queryset):
        for user in queryset:
            user.delete()

        deleted_teams = 0
        for team in TeamInformation.objects.all():
            if team.Students.count() == 0:
                deleted_teams += 1
                team.delete()

        if deleted_teams > 0:
            self.message_user(request,
                          f"Deleted {deleted_teams } Teams as they had 0 students after executing "
                          f"'Deleting Selected Students' action")

    # Executed for deleting one student
    def delete_model(self, request, obj):
        obj.delete()
        deleted_teams = 0
        for team in TeamInformation.objects.all():
            if team.Students.count() == 0:
                deleted_teams += 1
                team.delete()

        if deleted_teams > 0:
            self.message_user(request,
                              f"Deleted {deleted_teams} Teams as they had 0 students after executing "
                              f"'Deleting Selected Students' action")

    new_student = True

    def save_model(self, request, obj, form, change):
        for student in Student.objects.all():
            if student.FullName == obj.FullName:
                self.new_student = False
        super().save_model(request, obj, form, change)

    def _response_post_save(self, request, obj):
        # Loop through all the user information objects
        if self.new_student:
            self.message_user(request, f"New")
            teaminfo = TeamInformation()
            teaminfo.save()

            teaminfo.Students.add(obj)

            teamId = TeamInformation.objects.get(TeamID=teaminfo.teamid)

            # Create new default Presentation Log object
            log = PresentationLog(TeamID=teamId)
            log.save()
            self.new_student = True
        else:
            self.message_user(request, f"Existing")
            self.new_student = False

        # Credit to https://docs.djangoproject.com/en/1.8/_modules/django/contrib/admin/options/
        opts = self.model._meta
        if self.has_change_permission(request, None):
            post_url = reverse('admin:%s_%s_changelist' %
                               (opts.app_label, opts.model_name),
                               current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts},
                                             post_url)
        else:
            post_url = reverse('admin:index',
                               current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    # Executed when a csv file has been uploaded and generates data from it
    def import_csv_user(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            # Credit to https://stackoverflow.com/questions/62912039/uploading-csv-file-django-using-a-form
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')

            repeated_lines = 0
            header_line = True
            first_name_field = 1
            last_name_field = 0
            for line in lines:
                # Split fields in file by comma
                fields = line.split(',')
                # If header line, don't include it
                if header_line:
                    header_line = False
                else:
                    try:
                        # Check if student object already exists
                        if Student.objects.get(FullName=f"{fields[last_name_field]}, {fields[first_name_field]}"):
                            repeated_lines += 1
                        # if doesnt exist, create new student object
                        else:
                            self.add_student(fields[last_name_field], fields[first_name_field])
                    # User has no objects so add everything
                    except ObjectDoesNotExist:
                        self.add_student(fields[last_name_field], fields[first_name_field])
                    except IndexError:
                        self.message_user(request, "Your csv file had blank lines, remove them and try again.")
                        form = CsvImportForm()
                        payload = {"form": form}
                        return render(
                            request, "csv_form.html", payload
                        )
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
    # Specifies the admin changelist template that we are extending to add an import csv link
    change_list_template = "admin/advisors_changelist.html"

    # Sorts by a Advisors Name field when displaying objects in Advisor admin page
    ordering = ('Name',)

    # Adds a new url to mainForm's urls.py that can direct the user to a form to import a csv file
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv-advisor/', self.import_advisor_csv),
        ]
        return my_urls + urls

    # Executed when a csv file has been uploaded and generates data from it
    def import_advisor_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            # Credit to https://stackoverflow.com/questions/62912039/uploading-csv-file-django-using-a-form
            file_data = csv_file.read().decode('utf-8')
            # Split lines in file by new line character
            lines = file_data.split('\n')

            repeated_lines = 0
            header_line = True
            line_number = 1
            first_name_field = 1
            last_name_field = 0
            for line in lines:
                # Split fields in file by comma
                fields = line.split(",")
                # If header line don't include it
                if header_line:
                    header_line = False
                else:
                    try:
                        # Check if object already exists
                        if Advisor.objects.get(Name=f"{fields[last_name_field]}, {fields[first_name_field]}"):
                            repeated_lines += 1
                        else:
                            # Create Advisor objects from passed in data
                            advisor = Advisor.objects.create(Name=f"{fields[last_name_field]}, {fields[first_name_field]}")
                            advisor.save()
                    # Advisor has no objects so add everything
                    except ObjectDoesNotExist:
                        # Create Advisor objects from passed in data
                        advisor = Advisor.objects.create(Name=f"{fields[last_name_field]}, {fields[first_name_field]}")
                        advisor.save()
                    except IndexError:
                        self.message_user(request, "Your csv file had a blank line at line " + str(line_number)
                                          + ", remove it and try again.")
                        form = CsvImportForm()
                        payload = {"form": form}
                        return render(
                            request, "csv_form.html", payload
                        )
                line_number += 1
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