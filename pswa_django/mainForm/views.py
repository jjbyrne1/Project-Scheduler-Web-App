from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from .forms import MyForm
from .models import User, PresentationLog, Advisor, TeamInformation


def showtable(request):
    if request.method == "POST":
        form = MyForm.MyForm()
        return render(request, "cv-form.html")
        #if form.is_valid:
        #    form.save()
        #return render(request, 'tableView.html', {'tableForm': form})
    else:
        form = MyForm.MyForm()
        advisor_list = Advisor.objects.all()
        user_list = User.objects.all()
        #user = user_list.get(TeamId__user=1)
        teaminfo_list = TeamInformation.objects.all()
        presentationlog_list = PresentationLog.objects.all()
        return render(request, 'tableView.html', {'tableForm': form, 'advisor_list': advisor_list, 'user_list': user_list,
                                                  'teaminfo_list': teaminfo_list,
                                                  'presentationlog_list': presentationlog_list})


class DateForm(forms.Form):
    #presentationinfo = PresentationLog.objects.all()
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])


def EditTeamInformation(request):
    advisor_list = Advisor.objects.all()
    user_list = User.objects.all()
    # user = user_list.get(TeamId__user=1)
    teaminfo_list = TeamInformation.objects.all()
    presentationlog_list = PresentationLog.objects.all()
    if request.method == "POST":
        form = MyForm.MyForm
        return render(request, 'tableView.html',
                      {'tableForm': form, 'advisor_list': advisor_list, 'user_list': user_list,
                       'teaminfo_list': teaminfo_list,
                       'presentationlog_list': presentationlog_list})
    else:
        form = MyForm.MyForm()
        return render(request, "cv-form.html")
        # if form.is_valid:
        #    form.save()
        # return render(request, 'tableView.html', {'tableForm': form})
