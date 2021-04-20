from django.shortcuts import render
from django import forms
from .models import User, PresentationLog, Advisor#, TeamInformation


def showtable(request):
    if request.method == "POST":
        form = forms.Form
        if form.is_valid:
            form.save()
        return render(request, 'tableView.html', {'form1': form})
    else:
        form = forms.Form
        advisor_list = Advisor.objects.all()
        user_list = User.objects.all()
        #user = user_list.get(TeamId__user=1)
        #teaminfo_list = TeamInformation.objects.all()
        presentationlog_list = PresentationLog.objects.all()
        return render(request, 'tableView.html', {'form1': form, 'advisor_list': advisor_list, 'user_list': user_list,
                                                  #'teaminfo_list': teaminfo_list,
                                                  'presentationlog_list': presentationlog_list})


class DateForm(forms.Form):
    #presentationinfo = PresentationLog.objects.all()
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])


def adduser(request, Name: str, Eid: str, Email: str):
    ti = TeamInformation.objects.create(numberOfTeamMembers=1)
    pl = PresentationLog.objects.create(teamID=ti.teamId)
    u = User.objects.create(name=Name, eid=Eid, password='', email=Email, teamID=ti.teamId, is_admin=False)
    ti.save()
    pl.save()
    u.save()
