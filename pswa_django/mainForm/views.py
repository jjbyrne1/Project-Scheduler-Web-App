from .forms import MyForm, UpdateTeamInformationForm
from django.shortcuts import render
from django import forms
from .forms.models import User, TeamInformation, PresentationLog


def showtable(request):
    if request.method == "POST":
        form = UpdateTeamInformationForm.UpdateTeamInformationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UpdateTeamInformationForm.UpdateTeamInformationForm()
    return render(request, 'tableView.html', {'form1': form})
    #return render(request, 'tableView.html')


class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])


def adduser(request, Name: str, Eid: str, Email: str):
    ti = TeamInformation.objects.create(numberOfTeamMembers=1)
    pl = PresentationLog.objects.create(teamID=ti.teamId)
    u = User.objects.create(name=Name, eid=Eid, password='', email=Email, teamID=ti.teamId, is_admin=False)
    ti.save()
    pl.save()
    u.save()


def my_form(request):
    if request.method == "POST":
        form = MyForm.MyForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MyForm.MyForm()
    return render(request, 'cv-form.html', {'form': form})


def my_form2(request):
    if request.method == "POST":
        form = UpdateTeamInformationForm.UpdateTeamInformationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UpdateTeamInformationForm.UpdateTeamInformationForm()
    return render(request, 'tableView.html', {'form1': form})
