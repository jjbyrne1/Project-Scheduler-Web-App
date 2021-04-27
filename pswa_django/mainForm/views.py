from django.shortcuts import render
from django import forms
from .models import User, PresentationLog, Advisor, TeamInformation


def showtable(request):
    if request.method == "POST":
        return render(request, "cv-form.html")
        #if form.is_valid:
        #    form.save()
        #return render(request, 'tableView.html', {'tableForm': form})
    else:
        advisor_list = Advisor.objects.order_by('Name')
        user_list = User.objects.order_by('FullName')
        teaminfo_list = TeamInformation.objects.order_by('TeamId')
        presentationlog_list = PresentationLog.objects.order_by('TeamId')
        return render(request, 'tableView.html', {'advisor_list': advisor_list, 'user_list': user_list,
                                                  'teaminfo_list': teaminfo_list,
                                                  'presentationlog_list': presentationlog_list})


class DateForm(forms.Form):
    #presentationinfo = PresentationLog.objects.all()
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])