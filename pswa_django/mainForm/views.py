from django.db.models import QuerySet
from django.shortcuts import render
from django import forms

from mainForm.models.model_advisors import Advisor
from mainForm.models.model_team_informations import TeamInformation
from mainForm.models.model_students import Student
from mainForm.models.model_presentation_logs import PresentationLog


def showtable(request):
    if request.method == "POST":
        return render(request, "tableView.html")
    else:
        advisor_list = Advisor.objects.order_by('FullName')
        student_list = Student.objects.order_by('FullName')
        teaminfo_list = TeamInformation.objects.order_by('TeamID')
        presentationlog_list = PresentationLog.objects.order_by('TeamID')
        return render(request, 'tableView.html', {'advisor_list': advisor_list,
                                                  'student_list': student_list,
                                                  'teaminfo_list': teaminfo_list,
                                                  'presentationlog_list': presentationlog_list})


class DateForm(forms.Form):
    #presentationinfo = PresentationLog.objects.all()
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
