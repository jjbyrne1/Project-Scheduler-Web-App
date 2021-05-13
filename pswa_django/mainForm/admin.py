from django import forms
from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from mainForm.models.model_advisors import Advisor
from mainForm.models.model_team_informations import TeamInformation
from mainForm.models.model_students import Student
from mainForm.models.model_presentation_logs import PresentationLog

# Credit to https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import models

# Credit to https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/
""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too """
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)

# Credit to https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/
""" Delete the file if something else get uploaded in its place """
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            # its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)

# Credit to https://cmljnelson.blog/2020/06/22/delete-files-when-deleting-models-in-django/
""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

"""
Registers the given model class (PresentationLog) with the given admin_class (PresentationLogAdmin).
"""
@admin.register(PresentationLog)
class PresentationLogAdmin(admin.ModelAdmin):
    # Sorts by a PresentationLog's TeamID field when displaying objects in PresentationLog admin page
    ordering = ('TeamID',)

"""
Registers the given model class (TeamInformation) with the given admin_class (TeamInformationAdmin).
"""
@admin.register(TeamInformation)
class TeamInformationAdmin(admin.ModelAdmin):
    # Sorts by a TeamInformation's TeamID field when displaying objects in TeamInformation admin page
    ordering = ('TeamID',)

    """ When multiple TeamInformation objects were selected to be deleted"""
    def delete_queryset(self, request, queryset):
        deleted_teams = 0
        for teaminfo in queryset:
            PresentationLog.objects.get(TeamID=teaminfo.teamid).delete()
            deleted_teams += 1

        if deleted_teams > 0:
            self.message_user(request,
                              f"Deleted {deleted_teams} Presentation Logs after executing "
                              f"'Delete Selected Team Information's action")

    """ When a TeamInformation object gets deleted"""
    def delete_model(self, request, obj: TeamInformation):
        PresentationLog.objects.get(TeamID=obj.teamid).delete()
        self.message_user(request,
                          f"Deleted corresponding PresentationLog with TeamID {obj.teamid}")

    """ After a TeamInformation object has been saved, check if any students """
    def _response_post_save(self, request, obj: TeamInformation):
        # Loop through all the team information objects
        for teaminfo in TeamInformation.objects.all().exclude(TeamID=obj.TeamID):
            # For each user in the changing objects User list
            for student in obj.Students.all():
                # For each User that was on the team before
                original_student: Student
                for original_student in teaminfo.Students.all():
                    if student.FullName == original_student.FullName:
                        t = TeamInformation.objects.get(TeamID=teaminfo.teamid)
                        t.Students.remove(student)
                        t.save()
                        if t.Students.count() == 0:
                            PresentationLog.objects.get(TeamID=teaminfo.teamid).delete()

        """ 
        Uncomment the below code if you want teams to be removed after all users are removed when
        saving a team information object
        """

        #if obj.Students.count() == 0:
        #    self.message_user(request, "in")
        #    obj.delete()

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


"""
Registers the given model class (Student) with the given admin_class (StudentAdmin).
"""
# Credit to https://books.agiliq.com/projects/django-admin-cookbook/en/latest/import.html
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Specifies the admin changelist template that we are extending to add an import csv link
    change_list_template = "admin/users_changelist.html"

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

        log = PresentationLog()
        log.save()

        logid = PresentationLog.objects.get(TeamID=log.logid)

        teaminfo = TeamInformation(TeamID=logid)
        teaminfo.save()

        teaminfo.Students.add(student)

    # Executed for deleting multiple students
    def delete_queryset(self, request, queryset):
        deleted_teams = 0
        students_on_deleted_team = False
        removed_students_from_teams = 0
        for student in queryset:
            team: TeamInformation
            for team in TeamInformation.objects.all():
                team_member: Student
                for team_member in team.Students.all():
                    if team_member.FullName == student.FullName:
                        students_on_deleted_team = True
                        student.delete()
                        if team.Students.count() >= 1:
                            removed_students_from_teams += 1
                            team.Students.remove(student)
                        else:
                            PresentationLog.objects.get(TeamID=team.teamid).delete()
                            deleted_teams += 1

        if not students_on_deleted_team:
            student_queryset: Student
            for student_queryset in queryset:
                Student.objects.get(FullName=student_queryset.FullName).delete()

        # Creating list of removed users
        string = ""
        b = True
        for student in queryset:
            if b:
                string = string + str(student)
                b = False
            else:
                string = string + "; " + str(student)

        if deleted_teams > 0:
            #self.message_user(request,
            #              f"Deleted corresponding TeamInformation with '{string}' on it")
            self.message_user(request,
                          f"Deleted {deleted_teams} Teams as they had 0 students after executing "
                          f"'Delete Selected Students' action")
        else:
            if removed_students_from_teams > 0:
                self.message_user(request,
                                  f"Removed '{string}' from their Teams")

    # Executed for deleting one student
    def delete_model(self, request, obj: Student):
        flag = False
        team: TeamInformation
        removed_student_from_team = 0
        deleted_team = 0
        for team in TeamInformation.objects.all():
            team_member: Student
            for team_member in team.Students.all():
                if team_member.FullName == obj.FullName:
                    flag = True
                    obj.delete()
                    if team.Students.count() >= 1:
                        removed_student_from_team = team.teamid
                        team.Students.remove(team_member)
                    else:
                        deleted_team = team.teamid
                        PresentationLog.objects.get(TeamID=team.teamid).delete()

        if not flag:
            Student.objects.get(FullName=obj.FullName).delete()
        else:
            if removed_student_from_team == 0:
                self.message_user(request,
                                  f"Deleted Team {deleted_team} as it had 0 students after deleting '{obj.FullName}'")
            else:
                self.message_user(request,
                                  f"Removed '{obj.FullName}' from Team {removed_student_from_team}")

    new_student = True

    """
    Student id is same then its not a new student.
    """
    def save_model(self, request, obj: Student, form, change):
        for student in Student.objects.all():
            if student.pk == obj.pk:
                self.new_student = False
                break
        super().save_model(request, obj, form, change)

    def _response_post_save(self, request, obj: Student):
        # Loop through all the user information objects
        if self.new_student:
            log = PresentationLog()
            log.save()

            logid = PresentationLog.objects.get(TeamID=log.logid)

            teaminfo = TeamInformation(TeamID=logid)
            teaminfo.save()

            teaminfo.Students.add(obj)
            self.new_student = True
        else:
            self.new_student = True

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
        try:
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
        except UnicodeDecodeError:
            messages.error(request, "Chosen file is not a .csv file type. Please insert a .csv file")
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
    ordering = ('FullName',)

    # Adds a new url to mainForm's urls.py that can direct the user to a form to import a csv file
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv-advisor/', self.import_advisor_csv),
        ]
        return my_urls + urls

    # Executed when a csv file has been uploaded and generates data from it
    def import_advisor_csv(self, request):
        try:
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
                            if Advisor.objects.get(FullName=f"{fields[last_name_field]}, {fields[first_name_field]}"):
                                repeated_lines += 1
                            else:
                                # Create Advisor objects from passed in data
                                advisor = Advisor.objects.create(FullName=f"{fields[last_name_field]}, {fields[first_name_field]}")
                                advisor.save()
                        # Advisor has no objects so add everything
                        except ObjectDoesNotExist:
                            # Create Advisor objects from passed in data
                            advisor = Advisor.objects.create(FullName=f"{fields[last_name_field]}, {fields[first_name_field]}")
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
                    self.message_user(request, "Your csv file has been successfully imported " + str(repeated_lines) +
                                      " repeats were detected and not added.")
                    return redirect("..")
                else:
                    self.message_user(request, "Your csv file has been successfully imported")
                    return redirect("..")
        except UnicodeDecodeError:
            messages.error(request, "Chosen file is not a .csv file type. Please insert a .csv file")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )