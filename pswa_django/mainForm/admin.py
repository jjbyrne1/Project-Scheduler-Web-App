from django.contrib import admin
from .models import User, PresentationLog, Advisor#, TeamInformation

# Register your models here.
admin.site.register(User)
#admin.site.register(TeamInformation)
admin.site.register(Advisor)
admin.site.register(PresentationLog)
